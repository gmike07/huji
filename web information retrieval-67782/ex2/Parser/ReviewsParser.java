package Parser;

import java.io.*;
import java.util.ArrayList;

public class ReviewsParser
{
    private static final int PID_LINE_FIRST_INDEX = 19;
    private static final String[] FIELDS_PREFIX = {
            "product/productId:", "review/userId:", "review/profileName:",
            "review/helpfulness:", "review/score:", "review/time:",
            "review/summary:", "review/text:", "product/productId:"
    };


    private BufferedReader reader;
    private String currentLine;
    private int current_field_index;

    public ReviewsParser(String path) {
        try {
            reader = new BufferedReader(new FileReader(path), 32768);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            System.exit(0);
        }
        currentLine = null;
    }

    /**
     * assuming correct structure of the input file
     * @return Review object if read successfully, otherwise null
     */
    public Review getNextReview()
    {
        String pid;
        int helpN, helpD;
        byte score;
        ArrayList<String> tokens;
        String fieldContent;
        current_field_index = 0;

        // read product id
        fieldContent = getNextField();
        if (fieldContent == null)
        {
            return null;
        }
        pid = fieldContent.substring(1);
        // read the user id
        getNextField();
        // read the profile name
        getNextField();
        // read the helpfulness
        fieldContent = getNextField();
        int[] helpfulness = parseHelpfulnessLine(fieldContent);
        helpN = helpfulness[0];
        helpD = helpfulness[1];
        // read the score
        fieldContent = getNextField();
        score = parseScoreLine(fieldContent);
        // raed the time
        getNextField();
        // read the summery
        getNextField();
        // read the text
        fieldContent = getNextField();
        tokens = parseTokensLine(fieldContent);
        return new Review(pid, helpN, helpD, score, tokens);
    }

    /**
     * assuming there is no field that contains a new line starting with the prefix of the next field
     * @param currentPrefixLength the length of the prefix of the current field
     * @param nextPrefix the prefix of the next field (after text should come product id)
     * @return the content of the current field
     */
    private String readNextField(int currentPrefixLength, String nextPrefix){
        String line = null;
        StringBuilder field;
        field = new StringBuilder();
        // if this is not our first read of the file
        if (currentLine != null)
        {
            line = currentLine;
        }
        else
        {
            try {
                line = reader.readLine();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        // if there is no more to read, empty line should return ""
        if (line == null)
        {
            return null;
        }
        field.append(line.substring(currentPrefixLength));
        while(true)
        {
            try {
                if (!((line = reader.readLine()) != null && (line.length() < nextPrefix.length() || !line.substring(0, nextPrefix.length()).equals(nextPrefix))))
                    break;
            } catch (IOException e) {
                e.printStackTrace();
            }
            field.append(line).append(" ");
        }
        // the first line of the next field
        currentLine = line;
        return field.toString();
    }


    private String getNextField() {
        String field = readNextField(FIELDS_PREFIX[current_field_index].length(), FIELDS_PREFIX[current_field_index + 1]);
        // turn the text field to lowercase
        if (current_field_index == 7)
        {
            field = field.toLowerCase();
        }
        if(current_field_index == 0)
        {
            field = field == null ? null : field.substring(0, 11);
        }
        current_field_index++;
        return field;
    }


    private static int[] parseHelpfulnessLine(String line)
    {
        int[] helpfulness = new int[2];
        int n, d;
        int slash_index = line.indexOf("/");
        n = Integer.parseInt(line.substring(1, slash_index));
        d = Integer.parseInt(line.substring(slash_index + 1));
        helpfulness[0] = n;
        helpfulness[1] = d;
        return helpfulness;
    }


    private static byte parseScoreLine(String line)
    {
        return Byte.parseByte(String.valueOf(line.charAt(1)));
    }


    private static ArrayList<String> parseTokensLine(String line)
    {
        int start = getNextTokenIndex(line, 0);
        int token_end_index;
        ArrayList<String> tokens = new ArrayList<>();
        while(start + 1 < line.length())
        {
            token_end_index = getNextToken(line, start);
            tokens.add(line.substring(start, token_end_index));
            start = getNextTokenIndex(line, token_end_index + 1);
        }
        return tokens;
    }

    /**
     *
     * @param line the whole text field content
     * @param start the index of the beginning of the current token
     * @return the index of the end of the current token (starting with index "start")
     */
    private static int getNextToken(String line, int start)
    {
        int i = start;
        while (isValidLetter(line.charAt(i)))
        {
            i++;
        }
        return i;
    }

    /**
     *
     * @param line the whole text field content
     * @param start the index of the end of the previous token
     * @return the index of the beginning of the next token
     */
    private static int getNextTokenIndex(String line, int start)
    {
        int i = start;
        while(i < line.length() && !isValidLetter(line.charAt(i)))
            i++;
        return i;
    }

    private static boolean isValidLetter(char l)
    {
        return Character.isLetterOrDigit(l);
    }


    public void closeSources() {
        try {
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
