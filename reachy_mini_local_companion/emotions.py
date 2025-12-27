"""Emotion display system for Reachy Mini.

Defines emotion profiles with coordinated head and antenna movements
for expressive robot behavior.
"""

from dataclasses import dataclass, field


@dataclass
class MovementKeyframe:
    """A single position in a movement sequence.

    Attributes:
        head_yaw: Head yaw angle in degrees (left/right).
        head_pitch: Head pitch angle in degrees (up/down).
        head_roll: Head roll angle in degrees (tilt).
        antenna_left: Left antenna angle in radians.
        antenna_right: Right antenna angle in radians.
        duration: Time to reach this position in seconds.
    """

    head_yaw: float = 0.0
    head_pitch: float = 0.0
    head_roll: float = 0.0
    antenna_left: float = 0.0
    antenna_right: float = 0.0
    duration: float = 0.3


@dataclass
class EmotionProfile:
    """Complete emotion definition with movement patterns.

    Attributes:
        name: Display name for the emotion.
        keyframes: Sequence of movement keyframes.
        sound: Optional sound file to play (without path).
        description: Short description of the emotion.
    """

    name: str
    keyframes: list[MovementKeyframe] = field(default_factory=list)
    sound: str | None = None
    description: str = ""


# ============================================================================
# Core Emotion Definitions
# ============================================================================

EMOTIONS: dict[str, EmotionProfile] = {
    "happy": EmotionProfile(
        name="Happy",
        description="Joyful nodding with perky antenna wiggles",
        sound="emotion_happy.wav",
        keyframes=[
            # Look up with antennas perked
            MovementKeyframe(head_pitch=10.0, antenna_left=0.4, antenna_right=0.4, duration=0.25),
            # Nod down
            MovementKeyframe(head_pitch=-5.0, antenna_left=-0.2, antenna_right=0.3, duration=0.2),
            # Nod up
            MovementKeyframe(head_pitch=8.0, antenna_left=0.3, antenna_right=-0.2, duration=0.2),
            # Quick wiggle
            MovementKeyframe(head_pitch=5.0, antenna_left=-0.3, antenna_right=0.4, duration=0.15),
            MovementKeyframe(head_pitch=5.0, antenna_left=0.4, antenna_right=-0.3, duration=0.15),
            # Return to neutral
            MovementKeyframe(duration=0.3),
        ],
    ),
    "sad": EmotionProfile(
        name="Sad",
        description="Slow downward droop with lowered antennas",
        sound="emotion_sad.wav",
        keyframes=[
            # Slow droop down
            MovementKeyframe(head_pitch=-15.0, head_roll=5.0, antenna_left=-0.4, antenna_right=-0.4, duration=0.6),
            # Hold sad position
            MovementKeyframe(head_pitch=-18.0, head_roll=3.0, antenna_left=-0.5, antenna_right=-0.5, duration=0.8),
            # Small sigh movement
            MovementKeyframe(head_pitch=-12.0, antenna_left=-0.3, antenna_right=-0.3, duration=0.4),
            # Return slowly
            MovementKeyframe(duration=0.5),
        ],
    ),
    "curious": EmotionProfile(
        name="Curious",
        description="Head tilt with asymmetric antenna positioning",
        sound="emotion_curious.wav",
        keyframes=[
            # Tilt head, one antenna up
            MovementKeyframe(head_roll=-15.0, head_pitch=5.0, antenna_left=0.5, antenna_right=-0.1, duration=0.35),
            # Hold curious pose
            MovementKeyframe(head_roll=-12.0, head_pitch=8.0, antenna_left=0.4, antenna_right=0.0, duration=0.5),
            # Tilt other way
            MovementKeyframe(head_roll=10.0, head_pitch=5.0, antenna_left=-0.1, antenna_right=0.4, duration=0.35),
            # Return
            MovementKeyframe(duration=0.3),
        ],
    ),
    "excited": EmotionProfile(
        name="Excited",
        description="Rapid head bobs with fast antenna oscillation",
        sound="emotion_excited.wav",
        keyframes=[
            # Fast bob up
            MovementKeyframe(head_pitch=12.0, antenna_left=0.5, antenna_right=0.5, duration=0.15),
            # Fast bob down
            MovementKeyframe(head_pitch=-5.0, antenna_left=-0.3, antenna_right=0.4, duration=0.12),
            # Bob up
            MovementKeyframe(head_pitch=10.0, antenna_left=0.4, antenna_right=-0.3, duration=0.12),
            # Bob down with yaw
            MovementKeyframe(head_pitch=-3.0, head_yaw=10.0, antenna_left=-0.4, antenna_right=0.5, duration=0.12),
            # Bob up other side
            MovementKeyframe(head_pitch=8.0, head_yaw=-10.0, antenna_left=0.5, antenna_right=-0.4, duration=0.12),
            # Final wiggle
            MovementKeyframe(head_pitch=5.0, antenna_left=-0.2, antenna_right=0.3, duration=0.1),
            MovementKeyframe(head_pitch=5.0, antenna_left=0.3, antenna_right=-0.2, duration=0.1),
            # Return
            MovementKeyframe(duration=0.25),
        ],
    ),
    "sleepy": EmotionProfile(
        name="Sleepy",
        description="Slow head droop with antennas gradually lowering",
        sound="emotion_sleepy.wav",
        keyframes=[
            # Start drooping
            MovementKeyframe(head_pitch=-5.0, antenna_left=0.1, antenna_right=0.1, duration=0.5),
            # More droop
            MovementKeyframe(head_pitch=-12.0, head_roll=8.0, antenna_left=-0.2, antenna_right=-0.2, duration=0.6),
            # Almost asleep
            MovementKeyframe(head_pitch=-18.0, head_roll=10.0, antenna_left=-0.4, antenna_right=-0.4, duration=0.7),
            # Small wake jolt
            MovementKeyframe(head_pitch=-5.0, head_roll=3.0, antenna_left=0.1, antenna_right=0.1, duration=0.3),
            # Droop again
            MovementKeyframe(head_pitch=-15.0, head_roll=8.0, antenna_left=-0.3, antenna_right=-0.3, duration=0.5),
            # Return
            MovementKeyframe(duration=0.4),
        ],
    ),
    "surprised": EmotionProfile(
        name="Surprised",
        description="Quick head back with antennas shooting up",
        sound="emotion_surprised.wav",
        keyframes=[
            # Quick startle back
            MovementKeyframe(head_pitch=15.0, antenna_left=0.5, antenna_right=0.5, duration=0.12),
            # Hold surprised
            MovementKeyframe(head_pitch=12.0, antenna_left=0.45, antenna_right=0.45, duration=0.4),
            # Small settle
            MovementKeyframe(head_pitch=8.0, antenna_left=0.3, antenna_right=0.3, duration=0.25),
            # Return
            MovementKeyframe(duration=0.3),
        ],
    ),
    "angry": EmotionProfile(
        name="Angry",
        description="Sharp head shakes with flattened antennas",
        sound="emotion_angry.wav",
        keyframes=[
            # Lower head, flatten antennas
            MovementKeyframe(head_pitch=-8.0, antenna_left=-0.4, antenna_right=-0.4, duration=0.2),
            # Sharp shake left
            MovementKeyframe(head_yaw=-20.0, head_pitch=-5.0, antenna_left=-0.5, antenna_right=-0.3, duration=0.15),
            # Sharp shake right
            MovementKeyframe(head_yaw=20.0, head_pitch=-5.0, antenna_left=-0.3, antenna_right=-0.5, duration=0.15),
            # Shake left again
            MovementKeyframe(head_yaw=-15.0, head_pitch=-8.0, antenna_left=-0.5, antenna_right=-0.4, duration=0.15),
            # Hold angry pose
            MovementKeyframe(head_pitch=-10.0, antenna_left=-0.4, antenna_right=-0.4, duration=0.4),
            # Return
            MovementKeyframe(duration=0.3),
        ],
    ),
    "confused": EmotionProfile(
        name="Confused",
        description="Alternating head tilts with asymmetric antenna movements",
        sound="emotion_confused.wav",
        keyframes=[
            # Tilt right
            MovementKeyframe(head_roll=12.0, head_pitch=5.0, antenna_left=0.3, antenna_right=-0.2, duration=0.3),
            # Tilt left
            MovementKeyframe(head_roll=-12.0, head_pitch=3.0, antenna_left=-0.2, antenna_right=0.3, duration=0.3),
            # Back right with pitch
            MovementKeyframe(head_roll=8.0, head_pitch=8.0, antenna_left=0.2, antenna_right=-0.1, duration=0.25),
            # Small shake
            MovementKeyframe(head_yaw=-10.0, head_roll=-5.0, antenna_left=-0.1, antenna_right=0.2, duration=0.2),
            MovementKeyframe(head_yaw=10.0, head_roll=5.0, antenna_left=0.2, antenna_right=-0.1, duration=0.2),
            # Return
            MovementKeyframe(duration=0.3),
        ],
    ),
}


def get_emotion_names() -> list[str]:
    """Get list of available emotion names."""
    return list(EMOTIONS.keys())


def get_emotion(name: str) -> EmotionProfile | None:
    """Get an emotion profile by name."""
    return EMOTIONS.get(name)


def list_emotions() -> list[dict[str, str]]:
    """Get list of emotions with names and descriptions."""
    return [
        {"name": emotion_id, "display_name": profile.name, "description": profile.description}
        for emotion_id, profile in EMOTIONS.items()
    ]
