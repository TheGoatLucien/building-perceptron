import numpy as np

class Perceptron:
    """Perceptron binaire a seuil, pour des cibles codees 0 et 1.

    X doit etre une matrice numerique (observations, variables) pour fit,
    ou un vecteur/une matrice pour predict. Appeler fit avant predict.
    """

    def __init__(self, learning_rate=0.01, n_epochs=50):
        """Definir la taille des corrections et le nombre de passes."""
        self.learning_rate = learning_rate
        self.n_epochs = n_epochs

    def net_input(self, X):
        """Calculer le score lineaire X @ weights + bias."""
        return np.dot(X, self.weights) + self.bias

    def predict(self, X):
        """Predire 1 pour un score positif ou nul, sinon 0."""
        return np.where(self.net_input(X) >= 0, 1, 0)

    def fit(self, X, y):
        """Apprendre en corrigeant les poids apres chaque observation.

        Chaque appel reinitialise le modele. errors_ compte les erreurs
        pendant chaque passe, pas les erreurs du modele final sur le test.
        L'ordre des observations est conserve; aucune convergence parfaite
        n'est garantie pour des donnees non lineairement separables.
        """
        n_features = X.shape[1]
        self.weights = np.zeros(n_features)
        self.bias = 0
        self.errors_ = []

        for epoch in range(self.n_epochs):
            errors = 0
            for xi, target in zip(X, y):
                erreur = target - self.predict(xi)
                self.weights += self.learning_rate * erreur * xi
                self.bias += self.learning_rate * erreur
                errors += int(erreur != 0)
            self.errors_.append(errors)
        return self