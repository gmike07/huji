#include "Fractal.h"
#include <boost/tokenizer.hpp>
#include <fstream>
#include <boost/filesystem.hpp>

#define USAGE_ERROR "Usage: FractalDrawer <file path>"
#define CSV_ENDING ".csv"
#define INVALID_INPUT "Invalid input"
#define ERROR 1
#define AMOUNT_OF_COLS 2
#define INT_CONVERSION_ERROR -1

/**
 * @param fractals a list of fractals to draw backwards
 */
void drawFractalsBackwards(const std::vector<Fractal*>& fractals)
{
    for (int i = (int) fractals.size() - 1; i >= 0; i--)
    {
        fractals[i]->initFractal();
        fractals[i]->drawFractal();
        std::cout << std::endl;
    }
}

/**
 * @param fractals fractals a list of fractals to free
 */
void freeFractals(std::vector<Fractal*>& fractals)
{
    for(const Fractal* fractal : fractals)
    {
        delete fractal;
    }
}

/**
 * @param s the string t o convert
 * @return the number if possible, else INT_CONVERSION_ERROR
 */
int convertStringToInt(const std::string& s)
{
    try
    {
        int value = std::stoi(s);
        std::string stringValue = std::to_string(value);
        if(stringValue != s && stringValue + '\r' != s)
        {
            return INT_CONVERSION_ERROR;
        }
        return std::stoi(s);
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
 * @param s the string to search
 * @param character the char to find
 * @return s.count(character)
 */
int countOccurences(const std::string& s, char character)
{
    int count = 0;
    for(char c : s)
    {
        if(c == character)
        {
            count++;
        }
    }
    return count;
}

/**
 * @param s the input line
 * @return a correct fractal pointer from the inputs if are correct, else nullptr
 */
Fractal* processLine(const std::string& s)
{
    if(countOccurences(s, ',') != AMOUNT_OF_COLS - 1)
    {
        return nullptr;
    }
    typedef boost::tokenizer<boost::char_separator<char>> tokenizer;
    boost::char_separator<char> sep{","};
    tokenizer tok{s, sep};
    std::vector<int> tokenized(0);
    int value;
    for(const std::string& token: tok)
    {
        value = convertStringToInt(token);
        if(value == INT_CONVERSION_ERROR || AMOUNT_OF_COLS <= tokenized.size())
        {
            return nullptr;
        }
        tokenized.push_back(value);
    }
    if(tokenized.size() != AMOUNT_OF_COLS)
    {
        return nullptr;
    }
    return FractalFactory::createFractal(FractalFactory::FractalType (tokenized[0]), tokenized[1]);
}

/**
 * @param reader an in stream file to parse
 * @return ERROR if an error occured and prints nothing, else prints all the data reversed
 */
int processFile(std::ifstream & reader)
{
    std::string line;
    std::vector<Fractal*> fractals(0);
    while (std::getline(reader, line))
    {
        Fractal* processed = processLine(line);
        if(processed == nullptr)
        {
            freeFractals(fractals);
            return ERROR;
        }
        fractals.push_back(processed);
    }
    drawFractalsBackwards(fractals);
    freeFractals(fractals);
    return 0;
}


int main(int argc, char* argv[])
{
    if(argc != 2)
    {
        std::cerr << USAGE_ERROR << std::endl;
        return ERROR;
    }
    boost::filesystem::path p(argv[1]);
    //if doesn't end well or can't read
    if(!boost::filesystem::exists(p) || !boost::filesystem::is_regular_file(p) 
       || !p.has_extension() || p.extension() != CSV_ENDING)
    {
        std::cerr << INVALID_INPUT << std::endl;
        return ERROR;
    }
    boost::filesystem::ifstream reader(p);
    //if one of the inputs in the file is wrong
    if(processFile(reader) == ERROR)
    {
        std::cerr << INVALID_INPUT << std::endl;
        return ERROR;
    }
    return 0;
}