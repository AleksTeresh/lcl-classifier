from response import Source
from classifier_types import Classifier


class ClassifyContext:
    def __init__(
        self,
        brt_preclassified: bool = False,
        tlp_preclassified: bool = False,
        is_batch: bool = False,
    ):
        self.is_batch = is_batch
        self.brt_preclassified = brt_preclassified
        self.tlp_preclassified = tlp_preclassified
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
                    "https://github.com/trocher/tlp_classifier",
                    "https://github.com/trocher/tlp_doc",
                ],
            ),
            Classifier.RE: Source(
                "re",
                "Round Eliminator",
                ["https://github.com/olidennis/round-eliminator"],
            ),
        }
