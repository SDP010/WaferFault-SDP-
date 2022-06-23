from sklearn.model_selection import train_test_split
from Preprocessing import Preprocessor
from Clustering import KMeanClustering
from Tuner import ModelFinder
from Model_Methods import model_operations
from Loder import Data_loader
from Logger import Applogger

class model_train:

    def __init__(self):
        self.logger = Applogger()

    def training_model(self):
        try:

            # getting the data from the source
            data_getter = Data_loader()
            data = data_getter.get_data()
            # print(data)

            """Doing the data preprocessing"""

            preprocessor= Preprocessor()
            data = preprocessor.remove_col(data,['Wafer'])


            # create separate label and feature
            X,Y = preprocessor.separate_label_feature(data, label_name='Output')

            # check if missing values are present in the dataset
            is_null_present = preprocessor.is_null_present(X)


            # if there is null values then impute them properly
            if (is_null_present):
                X = preprocessor.impute_missing_values(X)


            # check further which columns do not contribute to predictions
            # if the standard deviation for a column is zero, it means that the column has constant values
            # and they are giving the same output both for good and bad sensors
            # prepare the list of such columns to drop

            col_to_drop = preprocessor.get_columns_with_zero_std_deviation(X)
            # drop the columns
            X = preprocessor.remove_col(X, col_to_drop)


            """Clustering Approach"""

            kmeans = KMeanClustering()

            # using elbow plot ot find the number of cluster
            no_of_cluster = kmeans.elbow_plot(X)
            # print(no_of_cluster)

            # divide the data into the cluster
            X = kmeans.create_cluster(X ,no_of_cluster)

            # create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels'] = Y

            # getting the unique clusters from our dataset
            list_of_clusters = X['Cluster'].unique()

            """Finding the best ML Algorithm to fit on each cluster"""

            for cluster in list_of_clusters:
                cluster_data = X[X['Cluster'] == cluster]

                # Prepare the feature and Label columns
                cluster_features = cluster_data.drop(columns= ['Labels', 'Cluster'], axis= 1)
                cluster_label = cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size= 0.15, random_state=355)
                # print(x_train)
                # print(y_train)
                # print(x_test)
                # print(y_test)
                model_finder = ModelFinder()


                # getting the best model for each of the clusters

                best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)

                # saving the best model to the directory.
                file_op = model_operations()

                save_model = file_op.save_model(best_model, best_model_name + str(cluster))


        except Exception as e:
            raise e












