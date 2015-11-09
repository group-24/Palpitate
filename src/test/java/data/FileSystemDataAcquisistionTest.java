package data;

import org.hamcrest.BaseMatcher;
import org.hamcrest.Description;
import org.junit.Assert;
import org.junit.Test;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.SortedMap;

import static org.hamcrest.CoreMatchers.hasItem;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.CoreMatchers.not;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.Assert.assertTrue;

/**
 * Created by Timotej on 21-Oct-15.
 */
public class FileSystemDataAcquisistionTest {

    final FileSystemDatabase fsdb = new FileSystemDatabase("exampleData");
    final List<SubjectRawData> sd = fsdb.getSubjects();

    @Test
    public void getsASubject() {
        assertThat(sd.size(), not(0));
    }

    @Test
    public void getsSubject1() {
        Assert.assertThat(sd, hasItem(new BaseMatcher<SubjectRawData>() {
            public void describeTo(Description description) {
                description.appendText("should have contained subject with id 1");
            }

            public boolean matches(Object item) {
                if (item instanceof SubjectRawData) {
                    SubjectRawData subject = (SubjectRawData) item;
                    return subject.getId() == 1 && subject.getBpm() != null;
                }
                return false;
            }
        }));
    }

    @Test
    public void canReadBpmFile() throws FileNotFoundException {
        SortedMap<Double, Double> map = SubjectRawDataBuilder.bpmDataParse(
                                        new File("exampleData/Subject1/BPM.txt"));
        assertThat(map.size(), is(9));
        assertThat(map.get(22.106), is(79.7));
        assertThat(map.get(25.434), is(78.5));
        assertThat(map.firstKey(), is(19.971));
        assertThat(map.lastKey(), is(25.434));
    }
}
