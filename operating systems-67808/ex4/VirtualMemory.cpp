#include "VirtualMemory.h"
#include "PhysicalMemory.h"

#define SUCCESS 1
#define FAILURE 0

static inline uint64_t max(uint64_t a, uint64_t b)
{
    if(a < b)
    {
        return b;
    }
    return a;
}

static inline uint64_t min(uint64_t a, uint64_t b)
{
    if(a < b)
    {
        return a;
    }
    return b;
}

static inline uint64_t abs_difference(uint64_t a, uint64_t b)
{
    if(a < b)
    {
        return b - a;
    }
    return a - b;
}

void clearTable(uint64_t frameIndex)
{
    for (uint64_t i = 0; i < PAGE_SIZE; ++i)
    {
        PMwrite(frameIndex * PAGE_SIZE + i, 0);
    }
}

void VMinitialize()
{
    clearTable(0);
}

static inline uint64_t getFrameOffset(uint64_t virtualAddress, uint64_t height)
{
    return (virtualAddress >> (height * OFFSET_WIDTH)) & uint64_t(PAGE_SIZE - 1);
}

struct searchInfo
{
    uint64_t zeroFrame;
    uint64_t parentFrame;
    uint64_t offset;
    uint64_t maxFrameCount;
    uint64_t worstFrame;
    uint64_t worstFrameDist;
    uint64_t worstPage;
    const uint64_t virtualAddress;
    const uint64_t page;
    searchInfo(uint64_t _virtualAddress): zeroFrame(0), parentFrame(0), offset(0),
            maxFrameCount(0), worstFrame(0), worstFrameDist(0), worstPage(0),
            virtualAddress(_virtualAddress), page(_virtualAddress / uint64_t(PAGE_SIZE))
    {
    }

};


static inline void searchFreePageBaseCase(searchInfo& info, uint64_t currentPage,
        uint64_t currentFrame, uint64_t parentFrame, uint64_t offsetInParentFrame)
{
    //calculate distance to new page
    uint64_t distance = abs_difference(info.page, currentPage);
    uint64_t cyclic_distance = min(uint64_t(NUM_PAGES) - distance, distance);

    // update min distances
    if(cyclic_distance > info.worstFrameDist)
    {
        info.worstFrame = currentFrame;
        info.worstPage = currentPage;
        info.worstFrameDist = cyclic_distance;
        info.parentFrame = parentFrame;
        info.offset = offsetInParentFrame;
    }
}

static bool checkInPath(searchInfo& info, uint64_t targetFrame)
{
    // saves current frame in the path
    uint64_t currentFrame = 0;

    //loop through the path
    for(uint64_t i = TABLES_DEPTH; i > 0; i--)
    {
        // check the next frame
        uint64_t address = currentFrame * uint64_t(PAGE_SIZE) + getFrameOffset(info.virtualAddress, i);

        // if encountered the target frame - the result is true
        if(currentFrame == targetFrame)
        {
            return true;
        }

        // read the next frame
        word_t nextFrame;
        PMread(address, &nextFrame);

        //check for end of path
        if(nextFrame == 0)
        {
            return false;
        }

        // advance
        currentFrame = nextFrame;
    }
    return false;
}


static void searchFreePage(searchInfo& info, uint64_t currentVirtualAddress=0,
        uint64_t currentFrame=0, uint64_t height=TABLES_DEPTH, uint64_t parentFrame=0,
        uint64_t offset=0)
{
    if(info.zeroFrame != 0)
    {
        return;
    }

    // if we got to the bottom of the tree
    if(height == 0)
    {
        searchFreePageBaseCase(info, currentVirtualAddress, currentFrame, parentFrame, offset);
        return;
    }

    // save the pointer from the pageTable
    word_t nextFrame;

    // checks if the frame is full of zeros
    bool zeroFrame = true;

    // loop through the neighbours of the current page table
    for (uint64_t i = 0; i < PAGE_SIZE; ++i)
    {

        // address of the
        uint64_t address = currentFrame * uint64_t(PAGE_SIZE) + i;
        uint64_t nextVirtualAddress = (currentVirtualAddress * uint64_t(PAGE_SIZE)) + i;

        // go to the next address
        PMread(address, &nextFrame);
        if(nextFrame != 0)
        {

            //if there is a non-NULL child than the pageTable is not empty
            zeroFrame = false;

            // update the maximal page count
            info.maxFrameCount = max(nextFrame, info.maxFrameCount);

            //continue the search
            searchFreePage(info, nextVirtualAddress, nextFrame, height- 1, currentFrame, i);
        }
    }

    // if the table is an empty table
    if(zeroFrame && !checkInPath(info, currentFrame))
    {
        info.zeroFrame = currentFrame;
        info.parentFrame = parentFrame;
        info.offset = offset;
    }
}

static void replaceEvicted(searchInfo& info, uint64_t frame, uint64_t height, bool clear=true)
{
    // if it is a page table
    if(height != 1)
    {
        if(!clear)
        {
            return;
        }
        // declare a new page table full of zeros
        clearTable(frame);
    }
    else
    {
        // import from the virtual memory the correct address
        PMrestore(frame, info.page);
    }
}

static uint64_t evict(uint64_t virtualAddress, uint64_t height)
{

    // saves information about the graph
    searchInfo info(virtualAddress);

    // search the graph
    searchFreePage(info);

    // if there is an empty table (option 1)
    if(info.zeroFrame != 0)
    {
        // clear the parent's pointer from pointing on the empty table
        PMwrite(info.parentFrame * uint64_t(PAGE_SIZE) + info.offset, 0);
        replaceEvicted(info, info.zeroFrame, height, false);
        return info.zeroFrame;
    }

    // if the physical memory is not full yet (option 2)
    if(info.maxFrameCount + 1 < uint64_t(NUM_FRAMES))
    {
        replaceEvicted(info, info.maxFrameCount + 1, height);
        // return the evicted frame
        return info.maxFrameCount + 1;
    }

    // (option 3)
    // clear the parent's pointer from pointing on the replaced frame
    PMwrite(info.parentFrame * uint64_t(PAGE_SIZE) + info.offset, 0);

    // save the replaced frame to the disk
    PMevict(info.worstFrame, info.worstPage);

    //put page in the worst frame
    replaceEvicted(info, info.worstFrame, height);
    return info.worstFrame;
}


static uint64_t getAddress(uint64_t virtualAddress)
{

    // loop variables
    uint64_t currentFrame = 0;
    uint64_t address;
    word_t nextFrame;

    // loop through the tree until reaching the virtualAddress
    for(uint64_t height = TABLES_DEPTH; height > 0; height--)
    {
        address = currentFrame * uint64_t(PAGE_SIZE) + getFrameOffset(virtualAddress, height);

        // reads the information in the current page table
        PMread(address, &nextFrame);

        // in case of eviction
        if(nextFrame == 0)
        {
            nextFrame = evict(virtualAddress, height);
            PMwrite(address, nextFrame);
        }
        //continue the loop
        currentFrame = nextFrame;
    }

    address = currentFrame * uint64_t(PAGE_SIZE) + getFrameOffset(virtualAddress, 0);

    return address;
}


int VMread(uint64_t virtualAddress, word_t* value)
{
    // in case of invalid input
    if(uint64_t(VIRTUAL_MEMORY_SIZE) <= virtualAddress ||
       uint64_t(TABLES_DEPTH + 1) > uint64_t(NUM_FRAMES))
    {
        return FAILURE;
    }

    // get address of RAM
    uint64_t address = getAddress(virtualAddress);
    PMread(address, value);
    return SUCCESS;
}


int VMwrite(uint64_t virtualAddress, word_t value)
{
    // in case of invalid input
    if(uint64_t(VIRTUAL_MEMORY_SIZE) <= virtualAddress ||
       uint64_t(TABLES_DEPTH + 1) > uint64_t(NUM_FRAMES))
    {
        return FAILURE;
    }

    // get address of RAM
    uint64_t address = getAddress(virtualAddress);
    PMwrite(address, value);
    return SUCCESS;
}
