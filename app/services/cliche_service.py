"""
Cliche service for providing literary phrases.

This module provides functionality for generating random literary
cliches in Japanese.
"""
import random
from typing import List, Optional


class ClicheService:
    """
    A service that provides random literary cliches in Japanese.
    These are typically used as placeholder responses or to add literary flair to messages.
    """

    def __init__(self) -> None:
        """Initialize the Cliche service with a list of Japanese literary phrases."""
        self.cliches: List[str] = [
            "信じられているから走るのだ。少し考えてみよう。",
            "私はなんにも知りません。しかし、少し考えてみましょう。",
            "人間は、しばしば希望にあざむかれるが、少し考えてみよう。",
            "私は、ひとの恋愛談を聞く事は、あまり好きでない。しかし、少し考えてみよう。",
            "あなたはさっきから、乙姫の居所を前方にばかり求めていらっしゃる。しかし、少し考えてみよう。",
            "恋愛は、チャンスではないと思う。少し考えてみよう。",
            "君のような秀才にはわかるまいが、少し考えてみよう。",
            "弱虫は、幸福をさえおそれるものです。しかし、少し考えてみましょう。",
            "信実とは、決して空虚な妄想ではなかった。少し考えてみよう。",
            "理窟はないんだ。しかし、少し考えてみよう。",
            "不良とは、優しさの事ではないかしら。しかし、少し考えてみよう。",
            "僕は今まで、説教されて、改心したことが、まだいちどもない。しかし、少し考えてみよう。",
            "怒る時に怒らなければ、人間の甲斐がありません。少し考えてみましょう。",
            "笑われて、笑われて、つよくなる。少し考えてみよう。",
        ]

    def get_random_cliche(self, exclude: Optional[List[str]] = None) -> str:
        """
        Return a random cliche from the collection.

        Args:
            exclude: Optional list of cliches to exclude from selection

        Returns:
            A randomly selected cliche phrase
        """
        if exclude:
            available_cliches = [c for c in self.cliches if c not in exclude]
            if not available_cliches:
                # If all cliches are excluded, fall back to the full list
                available_cliches = self.cliches
        else:
            available_cliches = self.cliches

        return random.choice(available_cliches)
