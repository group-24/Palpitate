package utils;

import com.google.common.primitives.Chars;
import org.hamcrest.core.IsCollectionContaining;

import static org.hamcrest.core.Is.is;
import static org.hamcrest.core.IsCollectionContaining.hasItem;
import static org.hamcrest.core.IsCollectionContaining.hasItems;
import static org.hamcrest.core.IsNot.not;
import org.junit.Test;

import java.text.StringCharacterIterator;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;

import static org.junit.Assert.*;

/**
 * Created by Timotej on 31-Oct-15.
 */
public class RandomStringTest {
    RandomString rndStr = new RandomString(RandomString.alphabetSize() + 1);

    @Test
    public void producesAnAlphaString() {
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('1')));
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('2')));
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('3')));
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('4')));
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('5')));
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('6')));
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('7')));
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('8')));
        assertThat(Chars.asList(rndStr.nextString().toCharArray()), not(hasItems('9')));
    }

    @Test
    public void producesAllUniqueStrings() {
        int size = 100;
        HashSet<String> hs = new HashSet<String>();
        for (int i = 0; i < size; i++) {
            hs.add(rndStr.nextString());
        }

        assertThat(hs.size(), is(size));
    }
}
