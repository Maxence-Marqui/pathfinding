# pathfinding
Comparateurs d'algorithms de pathfinding

Application utilisant Pygame pour représenter visuellement différents type d'algorithmes dans un tableau a nodes.

Les nodes jaunes et turquoises sont respectivement le début et la fin.
Celles noires sont les murs bloquant l'exploration.
Les vertes claires sont celles déja explorées.
Les vertes sombre sont les prochaines a être explorées si la fin n'est pas trouvée.

Ceux utilisés sont le Breadth-first search, qui fonctionne comme une vague s'étalant dans toutes les directions jusqu'à trouver la node finale.
Le Depth-first search choisit une directement choisie arbitrairement une direction ou chemin et explore le maximum possible dans cette direction. Si ce chemin est terminé sans trouver la fin il prendra la 2ème direction la plus éloignée possible que l'algo aura trouver lors de la première direction explorée.
Le Dijkstra utilise une fonction heuristique qui selectionne la node la plus éloignée du départ possible parmis celles explorable. Il a un fonctionnement semblable au BFS en tant normal mais il prend en compte la possibilité que certaines nodes soient plus couteuses a explorer.
Le A* utilise une fonction heuristique qui essaye d'explorer la direction diminuant au maximum la distance avec la node de fin tout en augmentant celle avec la node de départ.

Cette application permet également de sauvegarder les maps et les nommer avant de les stocker dans un fichier json pour les réutiliser dans le futur.
