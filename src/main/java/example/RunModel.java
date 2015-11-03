package example;

import database.DatabaseConnection;
import database.DatabaseDataset;
import database.NameDataInstancesBuilder;
import database.RawDataInstancesBuilder;
import ml.TrainingStatitistics;
import ml.models.regression.UserIndependentModel;
import weka.core.Instances;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Created by Timotej on 03-Nov-15.
 */
public class RunModel {

     public static void main(String args[]) throws Exception {
         Connection c = DatabaseConnection.getDatabaseConnection();
         System.out.println("Opened database successfully");

         NameDataInstancesBuilder ndib = new NameDataInstancesBuilder(
                                            new RawDataInstancesBuilder());
         DatabaseDataset<Instances> dataset = ndib.withFeature("f1").
                withFeature("f3").
                withFeature("BPM").
                build(c);
         UserIndependentModel model = new UserIndependentModel(dataset);
         TrainingStatitistics stats = model.train();
         System.out.println(stats);




    }
}
