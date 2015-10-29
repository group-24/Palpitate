package example;

import org.junit.Test;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.LinearRegression;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;

import java.util.ArrayList;
import java.util.Arrays;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.Assert.assertTrue;

/**
 * Created by Timotej on 29-Oct-15.
 */
public class WekaTestPlayground {
    Attribute x = new Attribute("x");
    Attribute y = new Attribute("y");

    @Test
    public void canClasifyTwoClasses() throws Exception {
        FastVector redBlack = new FastVector(2);
        redBlack.addElement("red");
        redBlack.addElement("black");
        Attribute classAttr = new Attribute("class", redBlack);

        FastVector atts = new FastVector(3);
        atts.addElement(x);
        atts.addElement(y);
        atts.addElement(classAttr);

        Instances dataset = new Instances("test", atts, 3);
        dataset.setClass(classAttr);

        Instance inst = new Instance(3);
        inst.setValue(x, 1);
        inst.setValue(y, 1);
        inst.setValue(classAttr, "black");
        dataset.add(inst);

        inst = new Instance(3);
        inst.setValue(x, -1);
        inst.setValue(y, -1);
        inst.setValue(classAttr, "red");
        dataset.add(inst);

        inst = new Instance(3);
        inst.setValue(x, -0.98);
        inst.setValue(y, -0.98);
        inst.setValue(classAttr, "red");
        dataset.add(inst);

        NaiveBayes model = new NaiveBayes();
        model.buildClassifier(dataset);

        inst = new Instance(2);
        inst.setValue(x, -0.99);
        inst.setValue(y, -0.99);
        inst.setDataset(dataset);
        // 0 is red, 1 is black
        assertTrue(model.distributionForInstance(inst)[0] > 0.9999);
        assertTrue(model.distributionForInstance(inst)[1] < 0.0001);


        inst = new Instance(2);
        inst.setValue(x, 0.99);
        inst.setValue(y, 0.99);
        inst.setDataset(dataset);

        // 0 is red, 1 is black
        assertTrue(model.distributionForInstance(inst)[1] > 0.9999);
        assertTrue(model.distributionForInstance(inst)[0] < 0.0001);

    }
}
