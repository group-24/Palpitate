package matchers;

import org.hamcrest.BaseMatcher;
import org.hamcrest.Description;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Timotej on 31-Oct-15.
 */
public class SqlDataTableMatcher extends BaseMatcher<String> {

    private final Set<Integer> features;
    private final Pattern selects;
    private Pattern featureWhereClause;
    private Pattern joins;

    public SqlDataTableMatcher(Set<Integer> features) {

        this.features = features;
        featureWhereClause = Pattern.compile("([a-zA-Z]+).featureid\\s*=\\s*(\\d+)");
        joins = Pattern.compile("data as ([a-zA-Z]+)\\s*(join)?");
        selects = Pattern.compile("\\s*,\\s*([a-zA-Z]+)\\.featurevalue");
    }

    public boolean matches(Object item) {
        if (item instanceof String) {
            String str = ((String) item).toLowerCase();
            Matcher whereClause = featureWhereClause.matcher(str);
            Matcher  joinClause = joins.matcher(str);
            Matcher selectClause = selects.matcher(str);

            Map<Integer, String> aliases = new HashMap<Integer, String>();

            while (whereClause.find()) {
                aliases.put(Integer.valueOf(whereClause.group(2)), whereClause.group(1));
            }

            //if there is jsut 1 feature this checks are irrelevant
            if (features.size() > 1) {
                while (joinClause.find()) {
                    if (!aliases.values().contains(joinClause.group(1))) {
                        return false;
                    }
                }
                while (selectClause.find()) {
                    if (!aliases.values().contains(selectClause.group(1))) {
                        return false;
                    }
                }
            }

            // all the feautes are in the where clause and
            return aliases.keySet().equals(features);
        }
        return false;
    }

    public void describeTo(Description description) {

    }
}
