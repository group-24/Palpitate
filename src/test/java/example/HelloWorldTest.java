package example;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;

import org.junit.Test;

/**
 * Created by Timotej on 17-Oct-15.
 */
public class HelloWorldTest {

    @Test
    public void canPrintWord() {
        assertThat(new HelloWorld().word(), is("Hello World"));
     }

}
