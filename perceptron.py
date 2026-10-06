import numpy as np

class Perceptron:

    def __init__(self, learning_rate=0.01, n_epochs=50):
        self.learning_rate = learning_rate      # indice : on range ce qu'on reçoit
        self.n_epochs = n_epochs

    def net_input(self, X):
        # score = produit scalaire entre X et les poids, + le biais
        return np.dot(X, self.weights) + self.bias

    def predict(self, X):
        # si score >= 0 -> 1, sinon -> 0
        return np.where(self.net_input(X) >= 0, 1, 0)

    def fit(self, X, y):
        n_features = X.shape[1]                 # nombre de colonnes
        self.weights = np.zeros(n_features)            # un poids par colonne, tous à 0
        self.bias = 0
        self.errors_ = []                       # le carnet de notes

        for epoch in range(self.n_epochs):                # chaque soirée
            errors = 0
            for xi, target in zip(X, y):        # chaque invité
                erreur = target - self.predict(xi) # calcul de l'erreur pour cet invité
                self.weights += self.learning_rate * erreur * xi # veut ajuster les poids en fonction de l'erreur
                self.bias += self.learning_rate * erreur # ajuste le biais de la même manière
                errors += int(erreur != 0) # incrémente le compteur si l'erreur n'est pas nulle
            self.errors_.append(errors) # enregistre le nombre d'erreurs pour cette époque
        return self # retourne l'objet entraîné