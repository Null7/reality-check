from collections import Counter
import time
import sys
import numpy as np

def pretty_print_review_and_label(i):
    print(types[i] + "\t:\t" + titles[i] + "...")

g = open('titles.txt', 'r', encoding="utf8") # read the titles
titles = list(map(lambda x:x[:-1].lower(),g.readlines()))
g.close()

g = open('types.txt', 'r', encoding="utf8") # read the types
types = list(map(lambda x:x[:-1].upper(),g.readlines()))
g.close()

class SentimentNetwork:
    def __init__(self, titles, labels, min_count = 10, polarity_cutoff = 0.1, hidden_nodes = 10, learning_rate = 0.1):
        """Create a SentimenNetwork
        Args:
            reviews(list) - List of titles
            labels(list) - List of FAKE/REAL labels
            hidden_nodes(int) - Number of nodes to create in the hidden layer
            learning_rate(float) - Learning rate to use while training
        
        """
        # Assign a seed to our random number generator to ensure we get
        # reproducable results during development 
        np.random.seed(1)

        # process the reviews and their associated labels so that everything
        # is ready for training
        self.pre_process_data(titles, labels, polarity_cutoff, min_count)
        
        # Build the network to have the number of hidden nodes and the learning rate that
        # were passed into this initializer. Make the same number of input nodes as
        # there are vocabulary words and create a single output node.
        self.init_network(len(self.vocab), hidden_nodes, 1, learning_rate)
        
    def pre_process_data(self, titles, labels, polarity_cutoff, min_count):
        
        # words count
        words_counts = Counter()
        real_counts = Counter()
        fake_counts = Counter()
        
        for i in range(len(labels) - 1):
            if(labels[i] == 'FAKE'):
                for word in titles[i].split(" "):
                    words_counts[word] += 1
                    fake_counts[word] += 1
            else:
                for word in titles[i].split(" "):
                    words_counts[word] += 1
                    real_counts[word] += 1
                    
        fake_ratios = Counter()

        for term,cnt in list(words_counts.most_common()):
            if(cnt > 20):
                fake_ratio = fake_counts[term] / float(real_counts[term]+0.1)
                fake_ratios[term] = fake_ratio
                
        for word,ratio in fake_ratios.most_common():
            if(ratio > 1):
                fake_ratios[word] = np.log(ratio)
            else:
                fake_ratios[word] = -np.log((1 / (ratio + 0.01)))
        
        # populate vocab with all of the words in the given reviews
        vocab = set()
        for title in titles:
            for word in title.split(" "):
                if(words_counts[word] > min_count):
                    if(word in fake_ratios.keys()):
                        if((fake_ratios[word] >= polarity_cutoff) or (fake_ratios[word] <= -polarity_cutoff)):
                            vocab.add(word)
                    else:
                        vocab.add(word)
                
                

        # Convert the vocabulary set to a list so we can access words via indices
        self.vocab = list(vocab)
        
        # populate label_vocab with all of the words in the given labels.
        label_vocab = set()
        for label in labels:
            label_vocab.add(label)
        
        # Convert the label vocabulary set to a list so we can access labels via indices
        self.label_vocab = list(label_vocab)
        
        # Store the sizes of th vocabularies.
        self.vocab_size = len(self.vocab)
        self.label_vocab_size = len(self.label_vocab)
        
        # Create a dictionary of words in the vocabulary mapped to index positions
        self.word2index = {}
        for i, word in enumerate(self.vocab):
            self.word2index[word] = i
        
        # Create a dictionary of labels mapped to index positions
        self.label2index = {}
        for i, label in enumerate(self.label_vocab):
            self.label2index[label] = i
            
    def init_network(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Store the learning rate
        self.learning_rate = learning_rate

        # Initialize weights

        # These are the weights between the input layer and the hidden layer.
        self.weights_0_1 = np.zeros((self.input_nodes,self.hidden_nodes))
    
        # These are the weights between the hidden layer and the output layer.
        self.weights_1_2 = np.random.normal(0.0, self.output_nodes**-0.5, 
                                                (self.hidden_nodes, self.output_nodes))
        
        # The input layer, a two-dimensional matrix with shape 1 x input_nodes
        self.layer_1 = np.zeros((1,hidden_nodes))
        
    #def update_input_layer(self, title):

        # clear out previous state, reset the layer to be all 0s
        #self.layer_0 *= 0
        
        # word in title.split(" "):
            #if(word in self.word2index.keys()):
                #self.layer_0[0][self.word2index[word]] += 1
                
    def get_target_for_label(self, label):
        if(label == 'FAKE'):
            return 1
        else:
            return 0
            
    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_output_2_derivative(self,output):
        return output * (1 - output)
    
    def train(self, input_titles, training_labels):
        
        training_titles = list()
        
        for title in input_titles:
            indices = set()
            for word in title.split(" "):
                if(word in self.word2index.keys()):
                    indices.add(self.word2index[word])
            training_titles.append(list(indices))
        
        
        # make sure out we have a matching number of titles and labels
        assert(len(training_titles) == len(training_labels))
        
        # Keep track of correct predictions to display accuracy during training 
        correct_so_far = 0

        # Remember when we started for printing time statistics
        start = time.time()
        
        # loop through all the given titles and run a forward and backward pass,
        # updating weights for every item
        for i in range(len(training_titles)):
            
            # Get the next title and its correct label
            title = training_titles[i]
            label = training_labels[i]
            
            ### Forward pass ###

            # Input Layer
            # self.update_input_layer(title)

            # Hidden layer
            self.layer_1 *= 0
            for index in title:
                self.layer_1 += self.weights_0_1[index]

            # Output layer
            layer_2 = self.sigmoid(self.layer_1.dot(self.weights_1_2))
            
            ### Backward pass ###

            # Output error
            layer_2_error = layer_2 - self.get_target_for_label(label) # Output layer error is the difference between desired target and actual output.
            layer_2_delta = layer_2_error * self.sigmoid_output_2_derivative(layer_2)

            # Backpropagated error
            layer_1_error = layer_2_delta.dot(self.weights_1_2.T) # errors propagated to the hidden layer
            layer_1_delta = layer_1_error # hidden layer gradients - no nonlinearity so it's the same as the error

            # Update the weights
            self.weights_1_2 -= self.layer_1.T.dot(layer_2_delta) * self.learning_rate # update hidden-to-output weights with gradient descent step
            for index in title:
                self.weights_0_1[index] -= layer_1_delta[0] * self.learning_rate # update input-to-hidden weights with gradient descent step

            # Keep track of correct predictions.
            if(layer_2 >= 0.5 and (label == 'FAKE')):
                correct_so_far += 1
            elif(layer_2 < 0.5 and label == "REAL"):
                correct_so_far += 1
            
            # For debug purposes, print out our prediction accuracy and speed 
            # throughout the training process. 
            elapsed_time = float(time.time() - start)
            reviews_per_second = i / elapsed_time if elapsed_time > 0 else 0
            
            # sys.stdout.write("\rProgress:" + str(100 * i/float(len(training_titles)))[:4] \
            #                  + "% Speed(reviews/sec):" + str(reviews_per_second)[0:5] \
            #                  + " #Correct:" + str(correct_so_far) + " #Trained:" + str(i+1) \
            #                  + " Training Accuracy:" + str(correct_so_far * 100 / float(i+1))[:4] + "%")
            if(i % 2500 == 0):
                print("")
    def test(self, testing_titles, testing_labels):
        """
        Attempts to predict the labels for the given titles,
        and uses the test_labels to calculate the accuracy of those predictions.
        """
        
        # keep track of how many correct predictions we make
        correct = 0

        # we'll time how many predictions per second we make
        start = time.time()

        # Loop through each of the given titles and call run to predict
        # its label. 
        for i in range(len(testing_titles)):
            pred = self.run(testing_titles[i])
            if(pred == testing_titles[i]):
                correct += 1
            
            # For debug purposes, print out our prediction accuracy and speed 
            # throughout the prediction process. 

            elapsed_time = float(time.time() - start)
            reviews_per_second = i / elapsed_time if elapsed_time > 0 else 0
            
            # sys.stdout.write("\rProgress:" + str(100 * i/float(len(testing_titles)))[:4] \
            #                  + "% Speed(reviews/sec):" + str(reviews_per_second)[0:5] \
            #                  + " #Correct:" + str(correct) + " #Tested:" + str(i+1) \
            #                  + " Testing Accuracy:" + str(correct * 100 / float(i+1))[:4] + "%")
    
    def run(self, title):
        """
        Returns a prediction for the given title.
        """
        # Run a forward pass through the network, like in the "train" function.
        
        # Input Layer
        # self.update_input_layer(title.lower())

        # Hidden layer
        self.layer_1 *= 0
        unique_indices = set()
        for word in title.lower().split(" "):
            if word in self.word2index.keys():
                unique_indices.add(self.word2index[word])
        for index in unique_indices:
            self.layer_1 += self.weights_0_1[index]

        # Output layer
        layer_2 = self.sigmoid(self.layer_1.dot(self.weights_1_2))
        
        if(layer_2[0] >= 0.5):
            return "FAKE"
        else:
            return "REAL"
			
if __name__ == "__main__":
	mlp = SentimentNetwork(titles[:-5000], types[:-5000], learning_rate=0.1)
	mlp.train(titles[:-5000],types[:-5000])
	print(mlp.run(str(sys.argv)))
	# return 'REAL' if new is real, 'FAKE' otherwise
        
