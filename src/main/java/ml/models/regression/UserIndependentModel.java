package ml.models.regression;

import database.DatabaseDataset;
import ml.TrainingStatitistics;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.LinearRegression;
import weka.core.Instances;

import java.util.Random;

/**
 * Created by Timotej on 31-Oct-15.
 * This is an user independent model of batchID 1
 */
public class UserIndependentModel {

    private final DatabaseDataset<Instances> dbDataset;
    private final int batchID = 1;

    public UserIndependentModel(DatabaseDataset<Instances> dataset) {
        this.dbDataset = dataset;
    }

    public TrainingStatitistics train() throws Exception {
        Instances dataset = dbDataset.getBatch(1, 0);

        // Percent split
      /*  double percent = 0.80;
        int trainSize = (int) Math.round(dataset.numInstances() * percent);
        int testSize = dataset.numInstances() - trainSize;
        Instances train = new Instances(dataset, 0, trainSize);
        //We keep this secret and safe to evaluate the model
        Instances test = new Instances(dataset, trainSize, testSize);*/

        //doing proper cross validation, becuase currently don't have enough data

        dataset.randomize(new Random(4235345));

        Classifier model = new LinearRegression();
        Evaluation eval = new Evaluation(dataset);

        int folds = 2;
        for (int n = 0; n < folds; n++) {
            Instances trainFold = dataset.trainCV(folds, n);
            Instances testFold = dataset.testCV(folds, n);

            model.buildClassifier(trainFold);
            Classifier clsCopy = Classifier.makeCopy(model);
            clsCopy.buildClassifier(trainFold);
            eval.evaluateModel(clsCopy, testFold);
        }


        return new TrainingStatitistics(eval);
    }
}
