import numpy as np
import random
import time

maxIterations = 3

# Stop if reaches max or when the centroids are no longer changing
def shouldStop(oldCentroids, centroids, iterations):
    if iterations >= maxIterations:
        return True
    elif oldCentroids == None:
        return False
    
    return np.allclose(oldCentroids, centroids)

# Check if all labels have values
def labelsFilled(labels):
    for key in labels:
        if len(labels[key]) == 0:
            return False
    return True

# If there is an empty label then replace that centroid with a new one
def reinitialize(dataSet, centroids, labels):
    for idx, key in enumerate(labels):
        if not labels[key]:
            centroids[idx] = tuple(np.random.randint(255, size=(1, 3))[0])

    #print("reinitialized centroids: {}".format(centroids))
    print("reinitialized")
    return centroids

# Label each point in the dataSet to its closest centroid
def getLabels(dataSet, centroids):
    points = np.array(dataSet)
    centroids = np.array(centroids)
    
    labels = {k:[] for k in range(len(centroids))}
    point_calculated = {}

    for point in points:
        
        if "".join(str(i) for i in point.tolist()) in point_calculated.keys():
            idx = point_calculated["".join(str(i) for i in point.tolist())]
            labels[idx].append(point.tolist())
        else:
            dist = []
            dist = [np.sqrt((point - centroid)**2).sum() for centroid in centroids]
            min_dist = min(dist)
            labels[dist.index(min_dist)].append(point.tolist())

            a = "".join(str(i) for i in point.tolist())
            point_calculated[a] = dist.index(min_dist)

    return labels

# Calculate the new centroids based on mean or median
def calculateCentroids(labels, mean=False):
    centroid = []
    if(mean == True):
        centroid = [tuple(np.array(labels[key]).mean(axis=0)) for key in labels]
    else:
        centroid = [tuple(np.median(labels[key], axis=0)) for key in labels]
    
    return centroid

def k_means(dataSet, k, mean=False):

    centroids = np.random.randint(255, size=(k, 3))
    centroids = [tuple(val) for val in centroids]

    time.sleep(1)
    iterations = 0
    oldCentroids = None

    while not shouldStop(oldCentroids, centroids, iterations):
        oldCentroids = centroids
        iterations += 1

        # Assign labels to each datapoint based on centroids
        labels = getLabels(dataSet, centroids)
        while not labelsFilled(labels):
            
            centroids = reinitialize(dataSet, centroids, labels)
            s_v = time.time()
            labels = getLabels(dataSet, centroids) 

        # Assign centroids based on datapoint labels
        centroids = calculateCentroids(labels, mean) 

    return centroids
