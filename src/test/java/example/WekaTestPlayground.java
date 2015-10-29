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
 *
 * This tests ensure that Weka is correctly set up.
 * It is also meant as a learning example for people getting started to work with Weka.
 *
 * It is a trivial example and most of this stuff can be done by some Weka provided utility classes.
 * For example when reading from the database the dataset construction is mostly done for you.
 *  */
public class WekaTestPlayground {

    /*
    Firstly we set up two attributes x and y, which will be our data points.
    They can take values of type double, becuase of the constructor used.
     */
    Attribute x = new Attribute("x");
    Attribute y = new Attribute("y");

    @Test
    public void canClasifyTwoClasses() throws Exception {

        /*
        classAttr is the attribute that will determine what class a certain data point belongs to.
        FastVector is a weka data structure, that is not synchronized and is therefore faster. It is
        used throughout the framework

        We will classify our points into red and black classes
         */
        FastVector redBlack = new FastVector(2);
        redBlack.addElement("red");
        redBlack.addElement("black");
        /*
        Here we used the Attribute(String, FastVector) constructor which means that classAtr can
        only take values of red and black. Otherwise we will get an exception
         */
        Attribute classAttr = new Attribute("class", redBlack);

        //The attributes for a certain dataset need to be put into a collection.
        FastVector atts = new FastVector(3);
        atts.addElement(x);
        atts.addElement(y);
        atts.addElement(classAttr);

        //Here we construct the dataset. Think of it as a relational table test(x,y,classAttr)
        //We tell it, it will have 3 elements
        Instances dataset = new Instances("test", atts, 3);
        //This tells weka on which attribute to classify
        dataset.setClass(classAttr);

        /*
        3 touples are added to the dataset below:
        (1,1,black)
        (-1,-1,red)
        (-0.98,-0.98,red)
        I tried doing it with just 2, but it is too litle to get any results from the model.
         */

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

        //NaiveBayes is just a random classifier model, that just happens to do the right thing here
        NaiveBayes model = new NaiveBayes();
        /*
        Model builds itself, based on the constructed dataset i.e. It learns how to predict classAtr
        based on x and y. We told it what attribute represents the classes with line:
         dataset.setClass(classAttr);
         */
        model.buildClassifier(dataset);

        //Construct instance (-0.99,-0.99) to see if the model classifies it correctly
        inst = new Instance(2);
        inst.setValue(x, -0.99);
        inst.setValue(y, -0.99);
        //It needs to be told what dataset it belongs to, because otherwise there are errors.
        inst.setDataset(dataset);
        // 0 is red, 1 is black
        /*
        We assert that that instance above has a high probability of being red and
        low probability of being black. There are other methods available to determine
        what does the model think about the instance, but they did not work in this case
         */
        assertTrue(model.distributionForInstance(inst)[0] > 0.9999);
        assertTrue(model.distributionForInstance(inst)[1] < 0.0001);

        /*
        Same as the previous example, just the case for the other class
         */
        inst = new Instance(2);
        inst.setValue(x, 0.99);
        inst.setValue(y, 0.99);
        inst.setDataset(dataset);

        // 0 is red, 1 is black
        assertTrue(model.distributionForInstance(inst)[1] > 0.9999);
        assertTrue(model.distributionForInstance(inst)[0] < 0.0001);

    }
}
