package processing.parsingRules;

public class ParsingFactory {
    /**
     * @param parser the sting to create the parsing rule from
     * @return the corresponding parsing rule to the string
     */
    private static IparsingRule getParsingRule(IparsingRule.ParserTypes parser){
        switch (parser){
            case SIMPLE:
                return new SimpleParsingRule();
            case ST_MOVIE:
                return new STmovieParsingRule();
            case ST_TV:
                return new STtvSeriesParsingRule();
            default:
                return null;
        }
    }

    /**
     * @param parser the sting to create the parsing rule from
     * @return the corresponding parsing rule to the string
     */
    public static IparsingRule getParsingRule(String parser){
        return getParsingRule(IparsingRule.ParserTypes.valueOf(parser));
    }
}
