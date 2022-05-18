#include "Barrier.h"
#include "MapReduceFramework.h"
#include <atomic>
#include <vector>
#include <cstdlib>
#include <pthread.h>
#include <iostream>
#include <string>

#define FAILURE 1
#define SYS_ERR "system error: "


static const std::uint64_t stageShift = 62;
static const std::uint64_t middleShift = 31;
static const std::uint64_t incMiddle = std::uint64_t(1) << middleShift;
static const std::uint64_t incMiddleRight = std::uint64_t(1) + incMiddle;
static const std::uint64_t maskRightPart = incMiddle - std::uint64_t(1);

static inline std::uint64_t startStage(stage_t stage)
{
    return (std::uint64_t(int(stage)) << stageShift);
}

static inline int getRightPart(std::uint64_t value)
{
    return (int) (value & maskRightPart);
}

static inline int getMiddlePart(std::uint64_t value)
{
    return (int) ((value >> middleShift) & maskRightPart);
}

static inline int getStagePart(std::uint64_t value)
{
    return (int) ((value >> stageShift) & std::uint64_t(3));
}


static void system_call_error(const std::string& s)
{
    std::cerr << SYS_ERR << s << std::endl;
    exit(FAILURE);
}

struct jobContext
{
    pthread_t* threads;
    const MapReduceClient& client;
    const InputVec& inputVec;
    int multiThreadLevel;
    std::atomic<int> id_counter;
    //2 bits of stage || 31 bits for next free job in map || 31 bits processed jobs
    std::atomic<std::uint64_t> atomic_data;
    //amount of values in the second vector
    std::atomic<int> number_mapped_values;
    std::vector<pthread_mutex_t> mutexes_per_vector;
    Barrier barrier;
    std::vector<std::vector<IntermediatePair>> intermediate_vectors;
    IntermediateMap shuffling_map;
    pthread_mutex_t emit3_mutex;
    OutputVec& outputVec;
    std::vector<K2*> reduce_keys;
    bool is_done;

    explicit jobContext(const MapReduceClient& _client, const InputVec& _inputVec,
            OutputVec& _outputVec, int _multiThreadLevel): threads(nullptr), client(_client),
            inputVec(_inputVec), multiThreadLevel(_multiThreadLevel), id_counter(0),
            atomic_data(startStage(stage_t::MAP_STAGE)), number_mapped_values(0),
            mutexes_per_vector(multiThreadLevel - 1, PTHREAD_MUTEX_INITIALIZER),
            barrier(multiThreadLevel), intermediate_vectors(multiThreadLevel - 1,
                    std::vector<IntermediatePair>()), emit3_mutex(PTHREAD_MUTEX_INITIALIZER),
                                    outputVec(_outputVec), reduce_keys(0), is_done(false)
    {}

    ~jobContext()
    {
        for(auto& mutex : mutexes_per_vector)
        {
            if (pthread_mutex_destroy(&mutex) != 0)
            {
                system_call_error("[[mutex]] error on pthread_mutex_destroy");
            }
        }
        if (pthread_mutex_destroy(&emit3_mutex) != 0)
        {
            system_call_error("[[emit3 mutex]] error on pthread_mutex_destroy");
        }
        delete[] threads;
    }

};

struct threadContext
{
    jobContext* context;
    int id;
    threadContext(jobContext* jobContext, int thread_id): context(jobContext), id(thread_id)
    {}
};

static inline std::uint64_t incMiddlePart(jobContext* jc)
{
    return jc->atomic_data.fetch_add(incMiddle);
}

static int addValueMapWithoutMutex(jobContext* jc, unsigned long id)
{
    // success locking the mutex
    if(jc->intermediate_vectors[id].empty())
    {
        return 0;
    }
    IntermediatePair pair = jc->intermediate_vectors[id].back();

    // get the key to add to the map and add it
    jc->intermediate_vectors[id].pop_back();

    // if it is not in the map yet, allocate vector for it
    if (jc->shuffling_map.count(pair.first) == 0)
    {
        jc->shuffling_map[pair.first] = std::vector<V2*>(0);
    }

    // add the value to the map
    jc->shuffling_map[pair.first].push_back(pair.second);
    return 1;
}

static int addValueMap(jobContext* jc, unsigned long id)
{
    if (pthread_mutex_lock(&(jc->mutexes_per_vector[id])) != 0)
    {
        system_call_error("[[Shuffle mutex]] error on pthread_mutex_lock");
    }

    int value = addValueMapWithoutMutex(jc, id);

    // unlock the mutex
    if (pthread_mutex_unlock(&(jc->mutexes_per_vector[id])) != 0)
    {
        system_call_error("[[Shuffle mutex]] error on pthread_mutex_unlock");
    }
    return value;
}


static void shuffle(jobContext* jc)
{

    // stores the current number of values in the map
    int valsInMap = 0;

    // add values to the map as long as the regular threads dont finish their jobs
    unsigned long i = 0;
    while(jc->barrier.countReachedBarrier() < jc->multiThreadLevel - 1)
    {
        valsInMap += addValueMap(jc, i);
        i++;
        if(i == jc->mutexes_per_vector.size())
        {
            i = 0;
        }
    }

    // inform the user that we switched stage to shuffle stage
    //2 || number of mapped values || vals in map
    auto x = startStage(stage_t::SHUFFLE_STAGE) + valsInMap;
    jc->atomic_data = x;
    // add values to the map as long as the values exist
    while(getRightPart(jc->atomic_data) < jc->number_mapped_values)
    {
        for (unsigned long i = 0; i < jc->mutexes_per_vector.size(); i++)
        {
            jc->atomic_data.fetch_add(addValueMapWithoutMutex(jc, i));
        }
    }
    // update the atomic data to:
    //3 || map size || 0
    for(auto& it: jc->shuffling_map)
    {
        jc->reduce_keys.push_back(it.first);
    }
    jc->atomic_data = startStage(stage_t::REDUCE_STAGE);
}

static void map(threadContext* threadContext)
{

    //MASK_STAGE_KEY = 1 in every place of staged bits
    auto jc = threadContext->context;
    auto current_job = getMiddlePart(incMiddlePart(jc));

    while(current_job < (int)jc->inputVec.size())
    {
        const InputPair& pair = jc->inputVec[current_job];

        jc->client.map(pair.first, pair.second, threadContext);

        // finished a key
        current_job = getMiddlePart(jc->atomic_data.fetch_add(incMiddleRight));
    }
}

static void reduce(jobContext* jc)
{
    auto current_job = getMiddlePart(incMiddlePart(jc));
    while(current_job < (int)jc->reduce_keys.size())
    {
        K2* key = jc->reduce_keys[current_job];
        std::vector<V2*>& values = jc->shuffling_map[key];
        jc->client.reduce(key, values, jc);

        // finished a key
        current_job = getMiddlePart(jc->atomic_data.fetch_add(incMiddleRight));
    }
}


static void* threadFunc(void* context)
{
    auto jc = (jobContext*) context;

    // get a unique ID for the current thread
    int id = jc->id_counter.fetch_add(1);

    // if you are the last thread - do the shuffling job
    if(id == jc->multiThreadLevel - 1)
    {
        shuffle(jc);
    }
    else
    {
        // init the thread context
        threadContext tc(jc, id);
        map(&tc);
    }

    // barrier
    jc->barrier.barrier();

    //reduce
    reduce(jc);
    return nullptr;
}


void emit2(K2* key, V2* value, void* context)
{

    // init
    auto tc = (threadContext*) context;
    int id = tc->id;
    jobContext* jc = tc->context;

    //lock
    if (pthread_mutex_lock(&(jc->mutexes_per_vector[id])) != 0)
    {
        system_call_error("[[Emit2 mutex]] error on pthread_mutex_lock");
    }

    //critical section
    jc->intermediate_vectors[id].push_back(IntermediatePair(key, value));

    //update that another key was processed
    jc->number_mapped_values.fetch_add(1);

    //unlock
    if (pthread_mutex_unlock(&(jc->mutexes_per_vector[id])) != 0)
    {
        system_call_error("[[Emit2 mutex]] error on pthread_mutex_lock");
    }
}


void emit3(K3* key, V3* value, void* context)
{
    auto jc = (jobContext*) context;
    if (pthread_mutex_lock(&(jc->emit3_mutex)) != 0)
    {
        system_call_error("[[Emit3 mutex]] error on pthread_mutex_lock");
    }

    //critical section
    jc->outputVec.push_back(OutputPair(key, value));

    //unlock
    if (pthread_mutex_unlock(&(jc->emit3_mutex)) != 0)
    {
        system_call_error("[[Emit3 mutex]] error on pthread_mutex_lock");
    }
}

JobHandle startMapReduceJob(const MapReduceClient& client,
                            const InputVec& inputVec, OutputVec& outputVec,
                            int multiThreadLevel)
{
    jobContext* job;
    try
    {
        job = new jobContext(client, inputVec, outputVec, multiThreadLevel);
        job->threads = new pthread_t[multiThreadLevel];
    }
    catch(std::bad_alloc& e)
    {
        system_call_error("[[Allocation]] error on allocation memory");
        return nullptr;
    }
    for(int i = 0; i < multiThreadLevel; i++)
    {
        if(pthread_create(job->threads + i, nullptr, threadFunc, job) != 0)
        {
            system_call_error("[[Allocation]] error on allocation thread memory");
            return nullptr;
        }
    }

    return job;
}

void waitForJob(JobHandle job)
{
    auto jc = (jobContext*) job;
    if(jc->is_done)
    {
        return;
    }
    for(int i = 0; i < jc->multiThreadLevel; i++)
    {
        pthread_join(jc->threads[i], nullptr);
    }
    jc->is_done = true;
}

void getJobState(JobHandle job, JobState* state)
{
    auto jc = (jobContext*) job;
    uint64_t atomic_data = jc->atomic_data;
    state->stage = stage_t(getStagePart(atomic_data));

    // return the percentage of the progress
    int total;
    if(state->stage == stage_t::UNDEFINED_STAGE)
    {
        state->percentage = 0;
        return;
    }
    if(state->stage == stage_t::MAP_STAGE)
    {
        total = jc->inputVec.size();
    }
    else if(state->stage == stage_t::SHUFFLE_STAGE)
    {
        total = jc->number_mapped_values;
    }
    else
    {
        total = jc->reduce_keys.size();
    }

    //processed keys
    int value = getRightPart(atomic_data);

    // division
    if(total == 0)
    {
        state->percentage = 100.0f;
        return;
    }
    state->percentage = ((float)(value)) / ((float) total) * 100.0f;
}

void closeJobHandle(JobHandle job)
{
    waitForJob(job);
    delete (jobContext*) job;
}