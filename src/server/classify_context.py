from response import Source
from classifier_types import *


class ClassifyContext:
    def __init__(self, brtPreclassified=False, tlpPreclassified=False, isBatch=False):
        self.isBatch = isBatch
        self.brtPreclassified = brtPreclassified
        self.tlpPreclassified = tlpPreclassified
        # TODO: this probably shouldn't be hardcoded here
        self.sources = {
            Classifier.CP: Source(
                "cp",
                "Automata-theoretic lens paper",
                [
                    "https://arxiv.org/abs/2002.07659",
                    "https://github.com/AleksTeresh/cyclepath-classifier",
                ],
            ),
            Classifier.BRT: Source(
                "brt",
                "Binary rooted tree classifier (database)",
                ["https://github.com/AleksTeresh/tree-classifications"],
            ),
            Classifier.RT: Source(
                "rt",
                "Rooted tree classifier",
                [
                    "https://arxiv.org/abs/2102.09277",
                    "https://github.com/jendas1/rooted-tree-classifier",
                ],
            ),
            Classifier.TLP: Source(
                "tlp",
                "TLP Classifier",
                [
                    "https://github.com/trocher/tlpClassifier",
                    "https://github.com/trocher/tlpDoc",
                ],
            ),
            Classifier.RE: Source(
                "re",
                "Round Eliminator",
                ["https://github.com/olidennis/round-eliminator"],
            ),
        }
