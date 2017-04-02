from preprocess_and_extract import *
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

feature_set_1, feature_set_2, labels = load_training_data()
unlabeled = [label == -1 for label in labels]

while Counter(unlabeled)[True] > 0:
    train_set_1 = [features[1] for features in enumerate(feature_set_1) if unlabeled[features[0]] is False]
    train_set_2 = [features[1] for features in enumerate(feature_set_2) if unlabeled[features[0]] is False]

    test_set_1 = [features[1] for features in enumerate(feature_set_1) if unlabeled[features[0]] is True]
    test_set_2 = [features[1] for features in enumerate(feature_set_2) if unlabeled[features[0]] is True]

    # LinearSVC with L1-based feature selection
    # The smaller C, the stronger the regularization.
    # The more regularization, the more sparsity.
    model1 = Pipeline([
        ('feature_selection', LinearSVC(penalty="l1", dual=False, tol=1e-3)),
        ('classification', LinearSVC())
    ])

    model2 = Pipeline([
        ('feature_selection', LinearSVC(penalty="l1", dual=False, tol=1e-3)),
        ('classification', LinearSVC())
    ])

    model1.fit(train_set_1, [label for label in labels if label != -1])
    model2.fit(train_set_1, [label for label in labels if label != -1])

    decisions1 = model1.decision_function(test_set_1)
    decisions2 = model2.decision_function(test_set_2)
    most_certain = max(abs(decisions1.extend(decisions2)))
    certainties1 = abs(decisions1) / most_certain
    certainties2 = abs(decisions2) / most_certain
    accepted1 = [certainties for certainties in enumerate(certainties1) if certainties[1] > 0.7]
    accepted2 = [certainties for certainties in enumerate(certainties2) if certainties[1] > 0.7]

