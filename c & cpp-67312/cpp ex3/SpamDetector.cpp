//
// Created by Mike Greenbaum on 1/11/2020.
//
#define NUM_OF_ARGUMENTS 4
#define DATABASE_PATH 1
#define MESSAGE_PATH 2
#define THRESHOLD_NUM 3
#define ERROR -1
#define INT_CONVERSION_ERROR -1
#define INVALID_INPUT "Invalid input"
#define USAGE_ERROR "Usage: SpamDetector <database path> <message path> <threshold>"
#define STRING_SPLIT_TOKEN ','
#define SPAM "SPAM"
#define NOT_SPAM "NOT_SPAM"
#include <string>
#include <iostream>
#include <boost/filesystem.hpp>
#include "HashMap.hpp"


/**
 * copied from cpp ex 2
 * @param s the string t o convert
 * @return the number if possible, else INT_CONVERSION_ERROR
 */
int convertStringToInt(const std::string& s)
{
    try
    {
        int value = std::stoi(s);
        if(value < 0)
        {
            return INT_CONVERSION_ERROR;
        }
        std::string stringValue = std::to_string(value);
        if(stringValue != s && stringValue + '\r' != s)
        {
            return INT_CONVERSION_ERROR;
        }
        return value;
    }
    catch (const std::invalid_argument& ia)
    {
        return INT_CONVERSION_ERROR;
    }

    catch (const std::out_of_range& oor)
    {
        return INT_CONVERSION_ERROR;
    }

    catch (const std::exception& e)
    {
        return INT_CONVERSION_ERROR;
    }
}

/**
 * @param s the string to convert to lower
 * @return the string converted to lower
 */
std::string toLowerString(const std::string& s)
{
    std::string temp;
    for(char c : s)
    {
        temp += tolower(c);
    }
    return temp;
}

/**
 * @param mapping the mapping to use to score each sub message
 * @param line the line to add to the mapping
 * @return whether the line is valid and correctly added to the map
 * @throws std::invalid argument if couldn't update the map
 */
bool parseLineDatabase(HashMap<std::string, int>& mapping, const std::string& line)
{
    int index;
    if(line.find(STRING_SPLIT_TOKEN) == std::string::npos)
    {
        return false;
    }
    index = line.find(STRING_SPLIT_TOKEN);
    std::string badCombination = line.substr(0, index);
    if(badCombination.empty())
    {
        return false;
    }
    int number = convertStringToInt(line.substr(index + 1, line.size() - index));
    if(number == INT_CONVERSION_ERROR)
    {
        return false;
    }
    mapping.insert(badCombination, number);
    return true;
}

/**
 * @param p the path of the file
 * @param mapping the mapping to use to score each sub message
 * @return ERROR if an error occured during parsing, else 0
 * @throws std::invalid argument if couldn't update the map
 */
int processDatabaseFile(const boost::filesystem::path& p, HashMap<std::string, int>& mapping)
{
    boost::filesystem::ifstream reader(p);
    std::string line;
    while(std::getline(reader, line))
    {
        if(!parseLineDatabase(mapping, toLowerString(line)))
        {
            return ERROR;
        }
    }
    return 0;
}

/**
 * @param message the string to find occurences
 * @param subSpam the sub string to search for
 * @return the amount of times subSpam appears in message
 */
int countOccurences(const std::string& message, const std::string& subSpam)
{
    int count = 0;
    int currentFind = 0;
    while(message.find(subSpam, currentFind) != std::string::npos)
    {
        currentFind = message.find(subSpam, currentFind);
        currentFind += (int) subSpam.length();
        count++;
    }
    return count;
}

/**
 * @param p the path of the file
 * @param mapping the mapping to use to score each sub message
 * @return the spamNumber of the message if no errors occured, else ERROR
 */
int processMessageFile(const boost::filesystem::path& p, HashMap<std::string, int>& mapping)
{
    boost::filesystem::ifstream reader(p);
    std::string line, message;
    while(std::getline(reader, line))
    {
        message += toLowerString(line) + '\n';
    }
    int spamNumber = 0;
    for(auto& pair : mapping)
    {
        spamNumber += countOccurences(message, pair.first) * pair.second;
    }
    return spamNumber;
}

/**
 * @param p the path of the file
 * @return whether the file exists and not a directory
 */
bool doesFileExist(const boost::filesystem::path& p)
{
    return boost::filesystem::exists(p) && boost::filesystem::is_regular_file(p);
}

/**
 * @param argv the inputs from the cmd
 * @param threshold the threshold to check
 * @return ERROR if the inputs are not valid, else the score of the spam
 * @throws std::bad_alloc() if the map was not created correctly
 * @throws std::invalid argument() if couldn't update the map in processDatabaseFile
 */
int checkValidityInput(char* argv[], int threshold)
{
    if(threshold <= 0)
    {
        return ERROR;
    }
    boost::filesystem::path messagePath(argv[MESSAGE_PATH]);
    boost::filesystem::path databasePath(argv[DATABASE_PATH]);
    if(!doesFileExist(databasePath) || !doesFileExist(messagePath))
    {
        return ERROR;
    }
    HashMap<std::string, int> mapping;
    if(processDatabaseFile(databasePath, mapping) == ERROR)
    {
        return ERROR;
    }
    int spamNumber = processMessageFile(messagePath, mapping);
    if(spamNumber < 0)
    {
        return ERROR;
    }
    return spamNumber;
}


int main(int argc, char* argv[])
{
    if(argc != NUM_OF_ARGUMENTS)
    {
        std::cerr << USAGE_ERROR << std::endl;
        return EXIT_FAILURE;
    }
    int threshold = convertStringToInt(argv[THRESHOLD_NUM]);
    try
    {
        int spamNumber = checkValidityInput(argv, threshold);
        if(spamNumber == ERROR)
        {
            std::cerr << INVALID_INPUT << std::endl;
            return EXIT_FAILURE;
        }
        std::cout << ((spamNumber >= threshold) ? SPAM : NOT_SPAM) << std::endl;
        return 0;
    }
    catch(const std::bad_alloc& e)
    {
        std::cerr << INVALID_INPUT << std::endl;
        return EXIT_FAILURE;
    }
    catch(const std::invalid_argument& e)
    {
        std::cerr << INVALID_INPUT << std::endl;
        return EXIT_FAILURE;
    }
    catch(const std::out_of_range& e)
    {
        std::cerr << INVALID_INPUT << std::endl;
        return EXIT_FAILURE;
    }
    return 0;
}

