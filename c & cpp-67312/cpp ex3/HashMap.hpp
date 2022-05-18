
// Created by Mike Greenbaum on 1/9/2020.
//

#ifndef EX3TRY1_HASHMAP_HPP
#define EX3TRY1_HASHMAP_HPP

#include <vector>
#include <exception>
#include <iostream>
#define MIN_LOAD_FACTOR 0.25
#define MAX_LOAD_FACTOR 0.75
#define INITIAL_CAPACITY 16
#define RESIZE_FACTOR 2

#define INVALID_KEY_ACCESS_AT "Error: the given key doesn't exist in the hashMap!\n"
#define INVALID_KEY_BUCKET_SIZE "Error: key must exist in map in order to get the size of it's bucket!\n"
#define INVALID_KEY_BUCKET_INDEX "Error: key must exist in map in order to get the index of it's bucket!\n"
#define INVALID_KEYS_VALUES_CTOR "Error: wrong size of keys or values\n"
#define ACCESS_MAP_NULL "Error: the hash map is not created correctly!\n"

/**
 * @class a hashMap class to represent an abstract map with template
 * @tparam KeyT the type of key
 * @tparam ValueT the type of value
 */
template <class KeyT, class ValueT> class HashMap
{
private:
    //typedef to refer to pair easier
    typedef std::pair<KeyT, ValueT> KeyValue;
    //typedef to refer to bucket easier
    typedef std::vector<KeyValue> Bucket;
public:

    /**
     * @brief the default constructor
     * @throws std::bad_alloc if allocation failed
     */
    HashMap(): _capacity(INITIAL_CAPACITY), _buckets(nullptr)
    {
        _tryAllocMemoryBuckets(false);
    }

    /**
     * @brief a ctor that gets keys and values and adds them to the map
     * @param keys the keys to add
     * @param values the value to add
     * @throws std::bad_alloc if allocation failed
     */
    HashMap(const std::vector<KeyT>& keys, const std::vector<ValueT>& values): HashMap()
    {
        if(keys.size() != values.size())
        {
            std::__throw_invalid_argument(INVALID_KEYS_VALUES_CTOR);
        }
        for(unsigned int i = 0; i < keys.size(); i++)
        {
            (*this)[keys[i]] = values[i];
        }
    }
    /**
     * @brief the copy constructor
     * @param m the map to copy
     */
    HashMap(const HashMap<KeyT, ValueT>& m): _size(m._size), _capacity(m._capacity), _buckets(nullptr)
    {
        if(this != &m)
        {
            _tryAllocMemoryBuckets(false);
            for(int i = 0; i < _capacity; i++)
            {
                _buckets[i] = m._buckets[i];
            }
        }
    }

    /**
     * @brief the move constructor
     * @param m the map to move
     */
    HashMap(HashMap<KeyT, ValueT> && m) noexcept: _size(m._size), _capacity(m._capacity), _buckets(m._buckets)
    {
        m._capacity = 0;
        m._size = 0;
        m._buckets = nullptr;
    }

    /**
     * @brief the default dtor
     */
    ~HashMap()
    {
        delete[] _buckets;
    }

    /**
     * @brief a getter for the size of the hash map
     * @return the current size of the hash map
     */
    int size() const noexcept
    {
        return _size;
    }

    /**
     * @brief a getter for the capacity of the hash map
     * @return the current capacity of the hash map
     */
    int capacity() const noexcept
    {
        return _capacity;
    }

    /**
     * @brief a getter for the load factor of the hash map
     * @return the current load factor of the hash map
     */
    double getLoadFactor() const noexcept
    {
        return (double) _size / _capacity;
    }

    /**
     * @brief returns the size of the bucket that contains key
     * @param key the key to access the bucket with
     * @return the size od the bucket that contains key
     * @throws std::invalid_argument if the key is not in the map
     */
    int bucketSize(const KeyT& key) const
    {
        if(!containsKey(key))
        {
            std::__throw_invalid_argument(INVALID_KEY_BUCKET_SIZE);
        }
        return _buckets[_calculateHashIndex(key)].size();
    }

    /**
     * @brief a getter for if the hash map is empty
     * @return true iff the hash map is empty
     */
    bool empty() const noexcept
    {
        return _size == 0;
    }

    /**
     * @brief clears the data in the hash map, if the capacity was updated, it will create a blank vector to
     * hold the new capacity
     * @param resize if the buckets should be re alloced
     * @throws std::invalid_argument if the map is null
     */
    void clear(bool resize = false, bool shouldDelete = true)
    {
        _size = 0;
        //if the size needs to change, change it and then there is no need to clear each block
        if(resize)
        {
            _tryAllocMemoryBuckets(shouldDelete);
        }
        for(int i = 0; i < _capacity; i++)
        {
            _buckets[i].clear();
        }
    }

    /**
     * @param key gets the key to check
     * @return true iff the key is in the hash map
     * @throws std::invalid_argument if the map is null
     */
    bool containsKey(const KeyT& key) const
    {
        _errorIfHashNull();
        const Bucket& bucket = _buckets[_calculateHashIndex(key)];
        for(const KeyValue& pair : bucket)
        {
            if(pair.first == key)
            {
                return true;
            }
        }
        return false;
    }

    /**
     * @param key the key to access with
     * @return a reference to the value of the key
     * @throws std::out_of_range() on failure if key is not in map
     */
    ValueT& at(const KeyT& key)
    {
        _errorIfHashNull();
        auto& bucket = this->_buckets[_calculateHashIndex(key)];
        for(KeyValue& pair : bucket)
        {
            if(pair.first == key)
            {
                return pair.second;
            }
        }
        std::__throw_out_of_range(INVALID_KEY_ACCESS_AT);
    }

    /**
     * @param key the key to access with
     * @return the value of the key
     * @throws std::out_of_range() on failure if key is not in map
     */
    ValueT at(const KeyT& key) const
    {
        _errorIfHashNull();
        auto& bucket = this->_buckets[_calculateHashIndex(key)];
        for(const KeyValue& pair : bucket)
        {
            if(pair.first == key)
            {
                return pair.second;
            }
        }
        std::__throw_out_of_range(INVALID_KEY_ACCESS_AT);
    }

    /**
     * @brief adds the key, value from the map
     * @param key the key to add
     * @param value the value to add
     * @return true iff the key, value was successfully added (with Resizing)
     * @throws std::invalid_argument if the map is null
     */
    bool insert(const KeyT& key, const ValueT& value)
    {
        if(containsKey(key))
        {
            return false;
        }
        if((_size + 1) > _upperLoadFactor * _capacity)
        {
            _resizeHashMap(RESIZE_FACTOR * _capacity);
        }
        _addPairToMap(key, value);
        return true;
    }

    /**
     * @brief deletes the key from the map
     * @param key the key to erase
     * @return true iff the key was successfully deleted (with Resizing)
     * @throws std::invalid_argument if the map is null
     */
    bool erase(const KeyT& key)
    {
        _errorIfHashNull();
        if(!_deleteValue(key))
        {
            return false;
        }
        if(_size < _lowerLoadFactor * _capacity)
        {
            _resizeHashMap(_capacity / RESIZE_FACTOR);
        }
        return true;
    }

    /**
     * @brief let the user write HashMap m = HashMap m1;
     * @param other the other hash map
     * @return a reference to self
     */
    HashMap& operator=(const HashMap<KeyT, ValueT>& other)
    {
        if(this == &other)
        {
            return *this;
        }
        _size = other._size;
        _capacity = other._capacity;
        _tryAllocMemoryBuckets(true);
        for(int i = 0; i < _capacity; i++)
        {
            _buckets[i] = other._buckets[i];
        }
        return *this;
    }

    /**
     * @brief lets us access and change values through hashmap[key]
     * @param key the key to access with
     * @return the value connected to this key, if the key doesn't exists, adds it
     * @throws std::invalid_argument if the map is null
     */
    ValueT& operator[](const KeyT& key) noexcept
    {
        if(containsKey(key))
        {
            return at(key);
        }
        insert(key, ValueT());
        //return the new created value
        Bucket& bucket = _buckets[_calculateHashIndex(key)];
        return bucket[bucket.size() - 1].second;
    }

    /**
     * @brief lets us access and change values through hashmap[key]
     * @param key the key to access with
     * @return the value connected to this key, if the key doesn't exists, adds it
     * @throws std::invalid_argument if the map is null
     */
    ValueT operator[](const KeyT& key) const noexcept
    {
        _errorIfHashNull();
        auto& bucket = this->_buckets[_calculateHashIndex(key)];
        for(const KeyValue& pair : bucket)
        {
            if(pair.first == key)
            {
                return pair.second;
            }
        }
        return ValueT();
    }

    /**
     * @brief return true iff the two maps are identical
     * @param other the other map to check
     * @return true iff the two maps are identical
     */
    bool operator==(const HashMap<KeyT, ValueT>& other) const
    {
        if(this->_size != other._size)
        {
            return false;
        }
        for(int i = 0; i < _capacity; i++)
        {
            for(const KeyValue& pair: _buckets[i])
            {
                if(!other.containsKey(pair.first) || (pair.second != other.at(pair.first)))
                {
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * @brief return true iff the two maps are not identical
     * @param other the other map to check
     * @return true iff the two maps are not identical
     */
    bool operator!=(const HashMap<KeyT, ValueT>& other) const
    {
        return !(*this == other);
    }

    /**
     * @class const_iterator this class represents a const iterator of the hash map
     */
    class const_iterator
    {
    public:
        //the type of it1 - it2
        typedef std::ptrdiff_t difference_type;
        // the type that is returned in the iterator
        typedef const std::pair<KeyT, ValueT> value_type;
        // the type of value pointer
        typedef value_type* pointer;
        // the type of value pointer
        typedef value_type& reference;
        //the type of the iterator
        typedef std::forward_iterator_tag iterator_category;


        /**
         * @brief constructor of const iterator
         * @param map the map to read
         * @param startPointer where to start reading from
         * @throws std::invalid_argument id the map is null
         */
        explicit const_iterator(const HashMap<KeyT, ValueT>& map, int startPointer = 0): _map(&map),
                                                                                         _currVector(startPointer),
                                                                                         _currIndexInVector(-1)
        {
            ++(*this);
        }

        /**
         * @brief copy ctor
         * @param it the iterator to copy
         */
        const_iterator(const const_iterator& it): _map(it._map),
                                                  _currVector(it._currVector),
                                                  _currIndexInVector(it._currIndexInVector)
        {
        }

        /**
         * @brief default dtor
         */
        ~const_iterator() = default;
        //

        /**
         * @return get the value in that location
         */
        reference operator*() const
        {
            return _map->_buckets[_currVector][_currIndexInVector];
        }

        /**
         * @return get the value in that location
         */
        pointer operator->() const
        {
            return &_map->_buckets[_currVector][_currIndexInVector];
        }

        /**
         * @return the reference to self after advancing
         */
        const_iterator& operator++()
        {
            _advance();
            return *this;
        }

        /**
         * @return the reference to self before advancing
         */
        const_iterator operator++(int)
        {
            const_iterator temp = *this;
            ++(*this);
            return temp;
        }

        /**
         * @param other the iterator to compare
         * @return if the iterators are equal
         */
        bool operator==(const const_iterator& other) const
        {
            return _map == other._map && _currVector == other._currVector
                   && _currIndexInVector == other._currIndexInVector;
        }

        /**
         * @param other the iterator to compare
         * @return if the iterators are not equal
         */
        bool operator!=(const const_iterator& other) const
        {
            return !(*this == other);
        }

        /**
         * @param other the iterator to copy
         * @return a reference to self after copying other
         */
        const_iterator& operator=(const const_iterator& other)
        {
            _map = other._map;
            _currIndexInVector = other._currIndexInVector;
            _currVector = other._currVector;
            return *this;
        }

    private:
        //the map of this iterator
        const HashMap<KeyT, ValueT>* _map;
        //the current vector to iter over
        int _currVector;
        //the current index of the pairs to point at
        int _currIndexInVector;

        /**
         * advances the iterator one time
         */
        void _advance()
        {
            if(_currVector >= _map->_capacity || _currVector < 0)
            {
                _currVector = _map->_capacity;
                _currIndexInVector = 0;
                return;
            }
            _currIndexInVector++;
            if(_currIndexInVector < (int)_map->_buckets[_currVector].size())
            {
                return;
            }
            _currIndexInVector = 0;
            _currVector++;
            while(_currVector < _map->_capacity && _map->_buckets[_currVector].empty())
            {
                _currVector++;
            }
        }
    };

    /**
     * @return a forward iterator pointing to the beginning of the data
     */
    const_iterator begin() const
    {
        return const_iterator(*this);
    }

    /**
     * @return a forward iterator pointing to the beginning of the data
     */
    const_iterator cbegin() const
    {
        return const_iterator(*this);
    }

    /**
     * @return a forward iterator pointing to the end of the data
     */
    const_iterator cend() const
    {
        return const_iterator(*this, _capacity);
    }

    /**
     * @return a forward iterator pointing to the end of the data
     */
    const_iterator end() const
    {
        return const_iterator(*this, _capacity);
    }

    /**
     * @brief returns the index of the key if exists, else throws an exception
     * @param key the key to access the bucket with
     * @return returns the index of the key if exists
     * @throws std::invalid_argument if the key is not in the map
     */
    int bucketIndex(const KeyT& key) const
    {
        if(!containsKey(key))
        {
            std::__throw_invalid_argument(INVALID_KEY_BUCKET_INDEX);
        }
        return _calculateHashIndex(key);
    }


private:
    //the current size of the map
    int _size = 0;
    //the maximal capacity of the map
    int _capacity = INITIAL_CAPACITY;
    //the lower load factor of this map
    static constexpr double _lowerLoadFactor = MIN_LOAD_FACTOR;
    //the upper load factor of this map
    static constexpr double _upperLoadFactor = MAX_LOAD_FACTOR;
    //a vector that holds all the buckets of the map
    Bucket* _buckets;
    //the hash function of this map
    std::hash<KeyT> _hashFunction;

    /**
     * @brief the index of the key in the map
     * @param key the key to check
     * @return the index of the key in the map
     */
    int _calculateHashIndex(const KeyT& key) const noexcept
    {
        return _hashFunction(key) & (_capacity - 1);
    }

    /**
     * @brief adds the (key, value) to the map
     * @param key the key to add
     * @param value the value to add
     * Assumes: _buckets != nullptr
     */
    void _addPairToMap(const KeyT& key, const ValueT& value)
    {
        _size++;
        _buckets[_calculateHashIndex(key)].push_back(KeyValue(key, value));
    }

    /**
     * @brief checks whether the hash is not created, if so throws an error
     * @throws std::invalid_argument if the hash map is null
     */
    void _errorIfHashNull() const
    {
        if(_buckets == nullptr)
        {
            std::__throw_invalid_argument(ACCESS_MAP_NULL);
        }
    }

    /**
     * @brief deletes the key from the map
     * @param key the key to erase
     * @return true iff the key was successfully deleted
     * Assumes: _buckets != nullptr
     */
    bool _deleteValue(const KeyT& key)
    {
        Bucket& bucket = _buckets[_calculateHashIndex(key)];
        for(auto it = bucket.begin(); it != bucket.end(); ++it)
        {
            if((*it).first == key)
            {
                bucket.erase(it);
                _size--;
                return true;
            }
        }
        return false;
    }

    /**
     * @brief tries to alloc memory to _buckets, if fails resets and throws exception
     * @throws std::bad_alloc
     */
    void _tryAllocMemoryBuckets(bool deleteOldMemory = true)
    {
        if(deleteOldMemory)
        {
            delete[] _buckets;
        }
        try
        {
            _buckets = new Bucket[_capacity];
        }
        catch(const std::bad_alloc& e)
        {
            _buckets = nullptr;
            _size = 0;
            _capacity = 1;
            throw e;
        }
    }

    /**
     * @brief resize the map to the new size, keeps all elements
     * @param capacity the new size of the map
     * @throws std::invalid_argument if the map is null
     */
    void _resizeHashMap(int capacity)
    {
        int currCapacity = _capacity;
        _capacity = std::max(capacity, 1);
        Bucket* currentBuckets = _buckets;
        clear(true, false);
        for(int i = 0; i < currCapacity; i++)
        {
            for(KeyValue& pair : currentBuckets[i])
            {
                _addPairToMap(pair.first, pair.second);
            }
        }
        delete[] currentBuckets;
    }
};

#endif //EX3TRY1_HASHMAP_HPP
