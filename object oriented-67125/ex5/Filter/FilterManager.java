package Filter;

import ErrorTypes.TypeOneError;
import filesprocessing.HelperFunctions;
import filesprocessing.Section;

import java.io.File;
import java.util.ArrayList;

public class FilterManager {

    private static final String DEFAULT_CASE = "all";

    /* the size filter with not decorator */
    private static Filter sizeFilter = new NotFilter(new SizeFilter());
    /* the name filter with not decorator */
    private static Filter nameFilter = new NotFilter(new NameFilter());
    /* the property filter with not decorator */
    private static Filter propertyFilter = new NotFilter(new PropertyFilter());
    /* the all filter with not decorator */
    private static Filter allFilter = new NotFilter(new AllFilter());
    /* all the filters in an array */
    private static Filter[] filters = {allFilter, sizeFilter, propertyFilter, nameFilter};



    /**
     * @param section the current section of this filter
     * @param files the files to filter
     * @return the files filtered
     */
    public static File[] filter(Section section, File[] files){
        return filter(section.getFilterCommand(), section.getFilterNumber(), files);
    }

    /**
     * @param filterLine the line of the filter input
     * @param lineNumber the line in which the filter is happening in
     * @param files the files to filter
     * @return the files filtered
     */
    private static File[] filter(String filterLine, int lineNumber, File[] files){
        if (filterLine.equals(DEFAULT_CASE)) //if it is default case, return everything
            return files;
        try {
            for(Filter filter : filters)
                if (filter.isThisFilterCommand(filterLine))
                    return filter.filter(filterLine, files);
        }catch (TypeOneError error){
            HelperFunctions.printWarning(lineNumber);
            return filter(DEFAULT_CASE, lineNumber, files);
        }
        //else unknown command
        HelperFunctions.printWarning(lineNumber);
        return filter(DEFAULT_CASE, lineNumber, files);
    }

}
