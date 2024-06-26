# ComfyUI Prompt Quill

Custom [ComfyUI](https://github.com/comfyanonymous/ComfyUI) Nodes for interacting with [Prompt Quill](https://github.com/osi1880vr/prompt_quill).

Integrate the power of Prompt Quill into ComfyUI workflows.

To use this properly, you would need a running Prompt Quill API reachable from the host that is running ComfyUI.

## Installation

1. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
2. git clone in the ```custom_nodes``` folder inside your ComfyUI installation or download as zip and unzip the contents to ```custom_nodes/prompt_quill_comfyui```.
3. Start/restart ComfyUI

**Or** 

use the [comfyui manager](https://github.com/ltdrdata/ComfyUI-Manager) "install via git url" https://github.com/osi1880vr/prompt_quill_comfyui.

![pic](.meta/InstallViaManager.png)

### Nodes

### PromptQuillGenerate

A node that gives an ability to query Prompt Quill via given prompt. 

### PromptQuillSailing

A node that does some real magic, based on the vast ocean of data Prompt Quill uses you go on a journey along the data and you find amazing prompts.
This is an exploration feature more than create a prompt for a fixed input. each time you call it, it will create a new prompt, based on the most far context from the last run.
Important: If you want to start a new journey from a new starting point you have to set journey_reset to true for at least one image and then back to false. Only that way you reset the journeys history on the Prompt Quill side. I did not yet find any better way as Comfyui is kind of stateless.

More nodes will follow soon
