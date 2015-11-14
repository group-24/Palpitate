package ml;

import weka.classifiers.Evaluation;

/**
 * Created by Timotej on 03-Nov-15.
 */
public class TrainingStatitistics {

    private final Evaluation eval;

    public TrainingStatitistics(Evaluation eval) {
        this.eval = eval;
    }

    @Override
    public String toString() {
        return eval.toSummaryString();
    }
}
