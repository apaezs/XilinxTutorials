# HLS Adder
## Learn the basics of HLS by creating a simple 4- bit shift register

A complete tutorial for creating a simple shift register using Vitis HLS and integrating it into a Vivado block design for the Urbana FPGA board.
 
---
## PRE-REQ: HLS_1_ADDER && HLS_2_COUNTER

## Required Software

**AMD Xilinx Vitis 2024.1 – Complete Suite**

Includes:
- Vivado Design Suite
- Vitis HLS
- Vitis IDE

⚠️ Make sure you install the complete suite, not individual tools.

---

## Optional Hardware

- Zybo Z7-10

---

## Recommended Background

- Basic proficiency in C/C++
- Basic understanding of digital logic

---

# Simple HLS Shift Register Tutorial

---

## Step 1: Launch Vitis

1. Open Vitis 2024.1
2. ⚠️ **Make sure you open Vitis, not Vitis HLS 2024.1.**

![Vitis application](imgs/app_ss.png)

You should see the following home screen.

![Vitis 2024.1 home screen](imgs/vitis_2024.1_open_screen.png)

---

## Step 2: Create a Workspace

1. Click **Open Workspace**.
2. Navigate to your preferred directory and create a folder called: `hls_register`
3. Select the folder and click **Open Folder**.

![Workspace selection](imgs/workspace_open.png)

---

## Step 3: Create an HLS Component

1. In the top-left corner, select **Create HLS Component**.
2. A setup window will appear:
   - Change the component name to `simple_shift_register`
   - Keep the component location unchanged


3. On the **Configuration File** page, do not change anything. Click **Next**.
4. On the **Source Files** page, do not change anything. Click **Next**.
5. On the **Hardware** page:
   - Search for `xc7z010clg400-1`
   - Select it and click **Next**


6. Leave the remaining settings as-is and click **Finish**.

You should now see the following screen but with the component called simple_shift_register.

![Component added](imgs/component_add.png)

---

## Step 4: Add Source and Testbench Files

In the top-right panel under `simple_register [HLS]`:

1. Right-click **Sources** → **Add Source File**
2. Create a new C++ file named: `simple_register.cpp`
3. Repeat the process for the testbench:
   - Right-click **Testbench** → **Add Test Bench File**
   - Name it: `simple_register_tb.cpp`


---

## Step 5: Add the HLS Code

Copy the following into `simple_shift_register.cpp`:

```cpp
#include <ap_int.h>

void shift4_top(
    ap_uint<1> dir,        // 0=left, 1=right
    ap_uint<1> serial_in,
    ap_uint<4> &led_out
)
{
#pragma HLS INTERFACE ap_none port=dir
#pragma HLS INTERFACE ap_none port=serial_in
#pragma HLS INTERFACE ap_none port=led_out
#pragma HLS INTERFACE ap_ctrl_none port=return

    // Persistent register → becomes FFs
    static ap_uint<4> reg = 0;

    // Shift every clock (HLS provides it)
    if (dir == 0)
        reg = (reg << 1) | serial_in;
    else
        reg = (reg >> 1) | (serial_in << 3);

    led_out = reg;
}

```

Now copy the following into `simple_shift_register_tb.cpp`:

```cpp
#include <iostream>
#include <ap_int.h>

// Prototype of your HLS function
void shift4_top(
    ap_uint<1> dir,
    ap_uint<1> serial_in,
    ap_uint<4> &led_out
);

int main()
{
    ap_uint<4> leds;

    std::cout << "---- SHIFT LEFT TEST ----" << std::endl;

    // Shift left 4 times with serial_in = 1
    for (int i = 0; i < 4; i++) {
        shift4_top(0, 1, leds);   // dir=0 (left), serial_in=1
        std::cout << "Cycle " << i
                  << " -> LEDs = 0b" << leds.to_string(2)
                  << std::endl;
    }

    std::cout << "\n---- SHIFT RIGHT TEST ----" << std::endl;

    // Shift right 4 times with serial_in = 0
    for (int i = 0; i < 4; i++) {
        shift4_top(1, 0, leds);   // dir=1 (right), serial_in=0
        std::cout << "Cycle " << i
                  << " -> LEDs = 0b" << leds.to_string(2)
                  << std::endl;
    }

    return 0;
}


```

---

## Step 6: Run C Simulation

1. In the bottom-right corner under **C SIMULATION**, select **Run**.
2. If prompted to enable the Code Analyzer, select **No thanks**.
3. After simulation completes, a terminal window should appear.
4. If everything is correct, it should print: `SIM PASSED`


---

## Step 7: Set the Top-Level Function

Before synthesis, we must define the top-level function.

In the top-left panel under `simple_shift_register [HLS]`:

1. Select **Settings**
2. Open `hls_config.cfg`
3. Search for **Top**.
4. Under **C Synthesis Sources**, click **Browse** and select: `simple_shift_register.cpp`


5. Click **OK**.

---

## Step 8: Run HLS Flow

Run the following steps in order:

1. Under **C Synthesis**, select **Run**
   - Terminal should end with: "Synthesis finished successfully"



2. Under **Package**, select **Run**
   - Output should say: "Package finished successfully"

3. Under **Implementation**, select **Run**
   - Ignore warnings
   - This may take a while
   - Output should say: "Implementation finished successfully"

---

# Vivado Integration

---

## Step 9: Create a Vivado Project

1. Open Vivado 2024.1.
2. On the home screen under **Quick Start**, select **Create Project**.
3. Project name: `hls_shift_register_tutorial`
4. Choose a project location
5. Project type: **RTL Project**
6. Skip **Add Sources** and **Add Constraints**
7. On the **Default Part** page, switch to the board tab and search for the Zybo Z7-10; select it


8. Click **Finish**.

---

## Step 10: Create Block Design

1. In the left panel, select **Create Block Design**.
2. When prompted, press **OK**.

![Block design](imgs/block_design.png)

---

## Step 11: Add HLS IP Repository

From the top menu:

1. Select **Tools** → **Settings**

![Tools settings](imgs/tools_settings.png)

In the settings window:

2. Expand **IP**
3. Select **Repository**


4. Click the **+** icon and navigate to your Vitis HLS project directory.
5. Select the folder named `ip` (see screenshot). It should be similar to the folder for the hls adder shown below.


![IP files](imgs/files.png)

6. Press **OK**, then **Apply**.

---

## Step 12: Add the Adder IP

Back in the block design:

1. Click the **+** icon in the diagram area

![Block IP selection](imgs/block_ip.png)

2. Search for **Shift4_top** and add it.
3. Right-click the IP block and select **Make External** to expose its inputs and outputs.

---

## Step 13: Create HDL Wrapper

In **Sources** → **Design Sources**:

1. Right-click `design_1`
2. Select **Create HDL Wrapper**
3. Choose **Let Vivado manage wrapper and auto-update**

![HDL wrapper](imgs/wrap.png)

4. Click **OK**.

---

## Step 14: Add Constraints

1. Right-click **Constraints** → **Add Sources**


2. Select **Add or Create Constraints**
3. Choose **Create File**
4. Name it: `constraints`
5. Click **Finish**
6. Open the newly created constraint file and paste the following:

```tcl
## ===== CLOCK FROM SWITCH 0 =====
set_property -dict { PACKAGE_PIN G15 IOSTANDARD LVCMOS33 } [get_ports { ap_clk_0 }]

## ===== RESET FROM SWITCH 1 =====
set_property -dict { PACKAGE_PIN P15 IOSTANDARD LVCMOS33 } [get_ports { ap_rst_0 }]

## ===== DIRECTION FROM SWITCH 2 =====
set_property -dict { PACKAGE_PIN W13 IOSTANDARD LVCMOS33 } [get_ports { dir_0 }]

## ===== SERIAL INPUT FROM SWITCH 3 =====
set_property -dict { PACKAGE_PIN T16 IOSTANDARD LVCMOS33 } [get_ports { serial_in_0 }]

## ===== LED OUTPUT =====
set_property -dict { PACKAGE_PIN M14 IOSTANDARD LVCMOS33 } [get_ports { led_out_0[0] }]
set_property -dict { PACKAGE_PIN M15 IOSTANDARD LVCMOS33 } [get_ports { led_out_0[1] }]
set_property -dict { PACKAGE_PIN G14 IOSTANDARD LVCMOS33 } [get_ports { led_out_0[2] }]
set_property -dict { PACKAGE_PIN D18 IOSTANDARD LVCMOS33 } [get_ports { led_out_0[3] }]


```

---

## Step 15: Build and Program

In the left panel:

1. Select **Run Synthesis**

![Run synthesis](imgs/viv_synth.png)

When synthesis completes:

2. Select **Run Implementation**
3. Then select **Generate Bitstream**
4. Once complete:
   - Ensure the Zybo Z7-10 board is plugged in
   - Select **Open Hardware Manager**

![Hardware manager](imgs/hard.png)

5. Click **Open Target** → **Auto Connect**

![Connected](imgs/connected.png)

6. Finally:
   - Select **Program Device**
   - Click **Program**

---

## Done!

You can now test your shift register using:
- Switches as inputs
- LEDs as outputs

---

