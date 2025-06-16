# Import dataclass utilities and typing annotations
from dataclasses import dataclass, field, asdict
from typing import List, Tuple
import json
import os

# Define a data structure for a Pin with its name, direction, and position relative to the block
@dataclass
class Pin:
    name: str                    # Name of the pin
    direction: str               # Direction: "input" or "output"
    position: Tuple[int, int]    # Position relative to the top-left corner of the block

# Define a data structure for a GDS block in the layout
@dataclass
class GDSBlock:
    name: str                    # Block name
    schematic: str               # Schematic
    constraint: str
    gds_path: str                # Path to the block's GDS file
    position: Tuple[int, int]    # Block's position in the overall layout
    size: Tuple[int, int]        # Width and height of the block
    pins: List[Pin] = field(default_factory=list)  # List of pins attached to this block

    # Convert the GDSBlock object to a dictionary for JSON serialization
    def to_dict(self):
        return {
            "name": self.name,
            "schematic": self.schematic,
            "Constraint": self.constraint,
            "gds_path": self.gds_path,
            "position": list(self.position),  # Convert tuple to list for JSON compatibility
            "size": list(self.size),          # Convert tuple to list
            "pins": [asdict(pin) for pin in self.pins]  # Convert each Pin to dict
        }

    # Create a GDSBlock object from a dictionary (e.g., when loading from JSON)
    @staticmethod
    def from_dict(data):
        # Convert each pin dictionary to a Pin object
        pins = [Pin(**pin) for pin in data.get("pins", [])]
        # Return a new GDSBlock instance
        return GDSBlock(
            name=data["name"],
            gds_path=data["gds_path"],
            position=tuple(data["position"]),  # Convert list to tuple
            size=tuple(data["size"]),
            pins=pins
        )

# Manage a collection of blocks stored in a project directory
class BlockManager:
    def __init__(self, project_path: str):
        self.project_path = project_path                        # Root directory of the project
        self.json_path = os.path.join(project_path, "blocks.json")  # Path to the blocks.json file
        self.blocks: List[GDSBlock] = []                        # Internal list of GDSBlock objects

    # Load blocks from the JSON file if it exists
    def load_blocks(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as f:
                data = json.load(f)                             # Load JSON data as a dictionary
                self.blocks = [GDSBlock.from_dict(b) for b in data.get("blocks", [])]

    # Save all blocks to the JSON file
    def save_blocks(self):
        data = {"blocks": [block.to_dict() for block in self.blocks]}  # Serialize blocks
        with open(self.json_path, "w") as f:
            json.dump(data, f, indent=4)                        # Save as indented JSON

    # Add a new block to the list and save the updated list
    def add_block(self, block: GDSBlock):
        self.blocks.append(block)       # Add block to memory
        self.save_blocks()              # Save to file

    # Update the position of a block identified by name
    def update_block_position(self, block_name: str, new_position: Tuple[int, int]):
        for block in self.blocks:
            if block.name == block_name:
                block.position = new_position  # Update position
                break
        self.save_blocks()              # Save changes to file

    # Add a new pin to a block by name
    def add_pin_to_block(self, block_name: str, pin: Pin):
        for block in self.blocks:
            if block.name == block_name:
                block.pins.append(pin)  # Add pin to the block
                break
        self.save_blocks()

    # Remove a pin from a block by pin name
    def remove_pin_from_block(self, block_name: str, pin_name: str):
        for block in self.blocks:
            if block.name == block_name:
                block.pins = [pin for pin in block.pins if pin.name != pin_name]  # Filter out the pin
                break
        self.save_blocks()
