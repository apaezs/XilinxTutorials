# HLS Adder
## Learn the basics of HLS by creating a simple adder

A complete tutorial for creating a simple adder using Vitis HLS and integrating it into a Vivado block design for the Urbana FPGA board.

---

## Required Software

**AMD Xilinx Vitis 2024.1 – Complete Suite**

Includes:
- Vivado Design Suite
- Vitis HLS
- Vitis IDE

⚠️ Make sure you install the complete suite, not individual tools.

---

## Optional Hardware

- Urbana FPGA Board

---

## Recommended Background

- Basic proficiency in C/C++
- Basic understanding of digital logic

---

# Simple HLS Adder Tutorial

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
2. Navigate to your preferred directory and create a folder called: `hls_adder_tutorial`
3. Select the folder and click **Open Folder**.

![Workspace selection](imgs/workspace_open.png)

---

## Step 3: Create an HLS Component

1. In the top-left corner, select **Create HLS Component**.
2. A setup window will appear:
   - Change the component name to `simple_adder`
   - Keep the component location unchanged

![Component name and location](imgs/name_loc.png)

3. On the **Configuration File** page, do not change anything. Click **Next**.
4. On the **Source Files** page, do not change anything. Click **Next**.
5. On the **Hardware** page:
   - Search for `xc7s50csg324-1`
   - Select it and click **Next**

![Hardware selection](imgs/hardware.png)

6. Leave the remaining settings as-is and click **Finish**.

You should now see the following screen.

![Component added](imgs/component_add.png)

---

## Step 4: Add Source and Testbench Files

In the top-right panel under `simple_adder [HLS]`:

1. Right-click **Sources** → **Add Source File**
2. Create a new C++ file named: `simple_adder.cpp`
3. Repeat the process for the testbench:
   - Right-click **Testbench** → **Add Test Bench File**
   - Name it: `simple_adder_tb.cpp`

Your setup should now look like this.

![Files created](imgs/files_created.png)

---

## Step 5: Add the HLS Code

Copy the following into `simple_adder.cpp`:

```cpp
#include <ap_int.h>

extern "C" void adder(
    ap_uint<4> a,
    ap_uint<4> b,
    ap_uint<5> &sum
) {
#pragma HLS INTERFACE ap_none port=a
#pragma HLS INTERFACE ap_none port=b
#pragma HLS INTERFACE ap_none port=sum
#pragma HLS INTERFACE ap_ctrl_none port=return

    sum = a + b;
}
```

Now copy the following into `simple_adder_tb.cpp`:

```cpp
#include <iostream>
#include <ap_int.h>

extern "C" void adder(ap_uint<4> a, ap_uint<4> b, ap_uint<5> &sum);

int main() {
    ap_uint<5> s;

    adder(3, 7, s);
    if (s != 10) return 1;

    adder(15, 1, s);
    if (s != 16) return 1;

    std::cout << "SIM PASSED\n";
    return 0;
}
```

---

## Step 6: Run C Simulation

1. In the bottom-right corner under **C SIMULATION**, select **Run**.
2. If prompted to enable the Code Analyzer, select **No thanks**.
3. After simulation completes, a terminal window should appear.
4. If everything is correct, it should print: `SIM PASSED`

![Simulation passed](imgs/sim_passed.png)

---

## Step 7: Set the Top-Level Function

Before synthesis, we must define the top-level function.

In the top-left panel under `simple_adder [HLS]`:

1. Select **Settings**
2. Open `hls_config.cfg`
3. Search for **Top**.
4. Under **C Synthesis Sources**, click **Browse** and select: `simple_adder.cpp`

![Settings configuration](imgs/settings.png)

5. Click **OK**.

---

## Step 8: Run HLS Flow

Run the following steps in order:

1. Under **C Synthesis**, select **Run**
   - Terminal should end with: "Synthesis finished successfully"

![Synthesis successful](imgs/synthesis_suc.png)

2. Under **C/RTL Co-Simulation**, select **Run**
   - Output should say: "Co-simulation finished successfully"

3. Under **Package**, select **Run**
   - Output should say: "Package finished successfully"

4. Under **Implementation**, select **Run**
   - Ignore warnings
   - This may take a while
   - Output should say: "Implementation finished successfully"

---

# Vivado Integration

---

## Step 9: Create a Vivado Project

1. Open Vivado 2024.1.
2. On the home screen under **Quick Start**, select **Create Project**.
3. Project name: `hls_adder_tutorial`
4. Choose a project location
5. Project type: **RTL Project**
6. Skip **Add Sources** and **Add Constraints**
7. On the **Default Part** page, search for: `xc7s50csga324-1`

![Part selection in Vivado](imgs/part_in_vivado.png)

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

![Add IP repository](imgs/add_ip.png)

4. Click the **+** icon and navigate to your Vitis HLS project directory.
5. Select the folder named `ip` (see screenshot).

![IP files](imgs/files.png)

6. Press **OK**, then **Apply**.

---

## Step 12: Add the Adder IP

Back in the block design:

1. Click the **+** icon in the diagram area

![Block IP selection](imgs/block_ip.png)

2. Search for **Adder** and add it.
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

![Add constraints](imgs/con1.png)

2. Select **Add or Create Constraints**
3. Choose **Create File**
4. Name it: `urbana`
5. Click **Finish**
6. Open the newly created constraint file and paste the following:

```tcl
############################################################
# RealDigital Urbana - HLS Adder (design_1_wrapper)
# a_0   <- SW[3:0]
# b_0   <- SW[7:4]
# sum_0 -> LED[4:0]
############################################################

############################
# Reset (tie to SW15)
############################
set_property -dict {PACKAGE_PIN A8 IOSTANDARD LVCMOS25} [get_ports ap_rst_0]

############################
# Adder input A (SW[3:0])
############################
set_property -dict {PACKAGE_PIN G1 IOSTANDARD LVCMOS25} [get_ports {a_0[0]}]
set_property -dict {PACKAGE_PIN F2 IOSTANDARD LVCMOS25} [get_ports {a_0[1]}]
set_property -dict {PACKAGE_PIN F1 IOSTANDARD LVCMOS25} [get_ports {a_0[2]}]
set_property -dict {PACKAGE_PIN E2 IOSTANDARD LVCMOS25} [get_ports {a_0[3]}]

############################
# Adder input B (SW[7:4])
############################
set_property -dict {PACKAGE_PIN E1 IOSTANDARD LVCMOS25} [get_ports {b_0[0]}]
set_property -dict {PACKAGE_PIN D2 IOSTANDARD LVCMOS25} [get_ports {b_0[1]}]
set_property -dict {PACKAGE_PIN D1 IOSTANDARD LVCMOS25} [get_ports {b_0[2]}]
set_property -dict {PACKAGE_PIN C2 IOSTANDARD LVCMOS25} [get_ports {b_0[3]}]

############################
# Adder output (LED[4:0])
############################
set_property -dict {PACKAGE_PIN C13 IOSTANDARD LVCMOS33} [get_ports {sum_0[0]}]
set_property -dict {PACKAGE_PIN C14 IOSTANDARD LVCMOS33} [get_ports {sum_0[1]}]
set_property -dict {PACKAGE_PIN D14 IOSTANDARD LVCMOS33} [get_ports {sum_0[2]}]
set_property -dict {PACKAGE_PIN D15 IOSTANDARD LVCMOS33} [get_ports {sum_0[3]}]
set_property -dict {PACKAGE_PIN D16 IOSTANDARD LVCMOS33} [get_ports {sum_0[4]}]

############################
# Board configuration
############################
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.CONFIG.UNUSEDPIN PULLUP [current_design]
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
   - Ensure the Urbana board is plugged in
   - Select **Open Hardware Manager**

![Hardware manager](imgs/hard.png)

5. Click **Open Target** → **Auto Connect**

![Connected](imgs/connected.png)

6. Finally:
   - Select **Program Device**
   - Click **Program**

---

## Done!

You can now test your adder using:
- Switches as inputs
- LEDs as outputs

---

