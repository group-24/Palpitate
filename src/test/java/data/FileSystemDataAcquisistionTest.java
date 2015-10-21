package data;

import org.hamcrest.BaseMatcher;
import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.junit.Assert;
import org.junit.Test;

import java.util.List;

import static org.hamcrest.CoreMatchers.hasItem;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.CoreMatchers.not;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.Assert.assertTrue;

/**
 * Created by Timotej on 21-Oct-15.
 */
public class FileSystemDataAcquisistionTest {

    FileSystemDataBase fsdb = new FileSystemDataBase("exampleData");
    List<SubjectRawData> sd = fsdb.getSubjects();

    @Test
    public void getsASubject() {
        assertThat(sd.size(),not(0));
    }

    @Test
    public void getsSubject1() {
        Assert.assertThat(sd,hasItem(new BaseMatcher<SubjectRawData>() {
            public void describeTo(Description description) {}

            public boolean matches(Object item) {
                if(item instanceof SubjectRawData) {
                    SubjectRawData subject = (SubjectRawData)item;
                    return subject.getId() == 1 && subject.getBpm() != null;
                }
                return false;
            }
        }));
    }
}
