# PowerSentry-DC: Real-Time IEC 61000-4-30 Class A Power Quality Analyzer and ITIC Ride-Through Sentinel for High-Density Data Centers

**Competition:** Microchip–DigiKey PolarFire® FPGA Design Contest 2026–27  
**Track:** Track 2: Connected Real-Time Systems  
**Development Platform:** Microchip PolarFire SoC Icicle Kit (`MPFS250T-FCVG484E`)  
**Design Environment:** Microchip Libero® SoC Design Suite, SoftConsole IDE, Linux Yocto / FreeRTOS  

---

## 1. Project Overview & Executive Summary

As AI/ML and HPC clusters push data center rack densities past 40–100 kW, electrical infrastructure faces two under-monitored risks. Standard Multi-Function Meters average voltage over 1-second to 10-minute windows, making them blind to brief voltage sags that breach ITIC/SEMI-F47 tolerance curves — these events deplete server power-supply holdup capacitors, triggering simultaneous multi-rack reboots with no forensic record of the cause. Separately, non-linear server power supplies inject triplen harmonics (3rd, 9th, 15th) that sum additively in the neutral conductor of 4-wire distribution systems rather than canceling, often reaching 140–170% of phase current — creating overheating and fire risk invisible to standard phase-only breaker monitoring.

PowerSentry-DC addresses both gaps on the Microchip PolarFire SoC Icicle Kit (MPFS250T). An 8-channel simultaneous-sampling AD7606 ADC feeds a deterministic FPGA DSP pipeline that recalculates sliding half-cycle RMS on every sample (10.24 kS/s), comparing live voltage against ITIC/SEMI-F47 curves and triggering a sub-10-microsecond hardware interrupt for protective shedding or UPS transfer before servers crash. A parallel 1024-point FFT pipeline computes harmonics to the 63rd order, true THD, and dynamic transformer K-factor, while directional harmonic power flow distinguishes utility-side pollution from internally generated server harmonics. Pre/post-fault waveforms are captured via on-chip LSRAM and DMA-streamed to LPDDR4 for forensic review.

A RISC-V AMP subsystem splits work cleanly: one FreeRTOS core handles deterministic event logging and Modbus-TCP for SCADA/PLC integration, while Linux cores host a web dashboard and MQTT gateway. Estimated FPGA resource utilization is under 10% across logic and DSP blocks, indicating strong feasibility within the contest timeline, with total additional prototype hardware cost under $40.

### 1.1 Innovation & Expected Impact

Commercial Class A power-quality analyzers rely on sequential microcontroller or multi-chip DSP+MCU architectures that struggle to sustain simultaneous multi-channel sampling, sliding RMS, FFT decomposition, and continuous oscillography without buffer overruns — and typically cost thousands of dollars per monitoring point, limiting deployment to a few shared panels per facility.

PowerSentry-DC's innovation is architectural: implementing the full DSP pipeline as deterministic, zero-jitter hardware logic on PolarFire's FPGA fabric, rather than software on a sequential processor, achieves hard real-time, sub-10-microsecond fault response at an embedded, low-cost footprint (under $40 in additional hardware beyond the kit). This shifts power-quality monitoring from a handful of expensive, centrally located instruments toward dense, per-rack or per-PDU deployment.

A key differentiator is directional harmonic active-power-flow calculation, which distinguishes utility-grid-origin pollution from internally generated server harmonics — letting facilities teams pinpoint root cause rather than merely detect symptoms, a diagnostic capability standard panel meters lack. Validation combines a Python/NumPy golden model of the IEC 61000-4-30 formulas (targeting agreement within 0.1% of the reference), recorded real-world fault playback (COMTRADE/PQDIF), and physical low-voltage benchtop testing — demonstrating rigor without requiring live high-voltage facility access.

Potential impact spans preventing costly multi-rack reboot events, reducing neutral-conductor fire risk, extending transformer life through K-factor-aware load management, and enabling facility-wide power-quality visibility at a fraction of traditional analyzer cost — directly scalable to every modern high-density data center, semiconductor fab, and industrial microgrid.

---

## 2. Industry Problem Statement & Motivation

### 2.1 The Invisible Voltage Sag Problem (5–10 Cycle Disasters)
Server power supplies incorporate bulk holdup capacitors designed to sustain DC bus voltage during brief power disruptions. Under the **ITIC (CBEMA)** and **SEMI-F47** power tolerance curves:
* Equipment must withstand complete voltage interruptions for up to **20 milliseconds** (1 cycle at 50 Hz).
* Equipment must withstand voltage sags down to **70% of nominal** for up to **500 milliseconds** (25 cycles).
* Equipment must withstand voltage sags down to **80% of nominal** for up to **10 seconds**.

However, when grid switching events, utility line faults, or nearby industrial motor starts cause a **5-to-10 cycle voltage sag down to 50%–60% of nominal**, server holdup capacitors deplete rapidly. Server power supplies trip on internal under-voltage lockout, causing thousands of blade servers and GPUs to crash simultaneously. Standard data center MFMs average voltages over 1 second, reporting a nominal reading (e.g., 228V instead of 230V) and completely failing to log the sub-cycle dip. Facilities engineers are left with "unexplained" server reboots and no actionable forensic data.

### 2.2 Reverse Harmonic Propagation & Neutral Conductor Overload
Modern data center power distribution follows a 7-stage power chain: *Utility Substations $\rightarrow$ MV Switchgear $\rightarrow$ Transformers $\rightarrow$ UPS Systems $\rightarrow$ Static Transfer Switches (STS) $\rightarrow$ Power Distribution Units (PDUs) $\rightarrow$ Server Racks*.

Conventional wisdom assumes that electrical disturbances originate from the utility grid and flow forward into the facility. In reality, modern data centers face severe **reverse harmonic propagation**:
* Thousands of active power factor correction (PFC) stages and rectifier circuits inside server racks inject 3rd, 5th, 7th, 9th, and 11th harmonic currents backwards into branch circuits and PDUs.
* **Triplen Harmonics ($3^{rd}, 9^{th}, 15^{th}, \dots$):** Because triplen harmonics are separated by $3 \times 120^\circ = 360^\circ$ (in phase with each other), they do not cancel in a 4-wire Wye distribution system. Instead, they **sum directly in the neutral conductor**:
  $$I_{\text{Neutral}} = \sqrt{I_{N,1}^2 + 3 \cdot \left( I_{A,3}^2 + I_{A,9}^2 + I_{A,15}^2 + \dots \right)}$$
* In high-density server halls, neutral currents frequently reach **$1.4\times$ to $1.7\times$ the phase current**. Because circuit breakers traditionally monitor only the three phase conductors, the neutral conductor can overheat, melt its insulation, and ignite electrical fires without tripping any protective devices.
* Excessive harmonic currents dramatically increase eddy current and stray load losses in distribution transformers, requiring continuous calculation of the **Transformer K-Factor**:
  $$K = \sum_{h=1}^{h_{\max}} I_h^2 \cdot h^2$$
  Operating standard transformers under high K-factor loads without derating results in rapid thermal degradation and catastrophic transformer failure.

### 2.3 Limitations of Conventional Microprocessor Solutions
Existing commercial Class A power quality analyzers rely on high-power x86 or multi-chip DSP+MCU architectures costing \$5,000–\$15,000 per monitoring point. Microcontrollers executing sequential interrupt routines cannot sustain simultaneous, multi-channel 10.24 kS/s sampling, sliding half-cycle RMS calculation, 1024-point FFT harmonic decomposition, and continuous oscillography without suffering buffer overruns and missing transient events.

The **Microchip PolarFire SoC** provides an architectural advantage: hard FPGA logic executes deterministic, zero-jitter math pipelines at hardware speeds, while the multi-core 64-bit RISC-V processor manages networking and high-level protocols—delivering industrial Class A performance at an embedded, low-power edge footprint.

---

## 3. System Architecture & Implementation

![PowerSentry-DC System Architecture Block Diagram](SYSTEM_BLOCK_DIAGRAM.png)

PowerSentry-DC is organized into three tightly coupled architectural tiers:
1. **Analog Signal Acquisition & Conditioning Tier**
2. **PolarFire FPGA Fabric Hardware Acceleration Tier (Libero SoC)**
3. **RISC-V Microprocessor Subsystem (MSS) Asymmetric Multiprocessing (AMP) Tier**

---

### 3.1 Analog Signal Acquisition & Interface
The analog front-end monitors 8 physical channels simultaneously:
* 3 Phase Voltages: $V_A, V_B, V_C$ (Line-to-Neutral / Line-to-Line)
* 3 Phase Currents: $I_A, I_B, I_C$
* 1 Neutral Conductor Current: $I_N$
* 1 Earth / Protective Conductor Current: $I_E$

**Hardware Interfacing:**
* **ADC:** Analog Devices **AD7606** 8-channel simultaneous-sampling 16-bit SAR ADC module.
* **Sampling Rate:** $10.24\text{ kS/s}$ per channel ($204.8\text{ samples/cycle}$ at 50 Hz nominal, $170.67\text{ samples/cycle}$ at 60 Hz).
* **Physical Connection:** The AD7606 evaluation board connects directly to the **40-Pin Raspberry Pi Header (J26/J27)** on the PolarFire SoC Icicle Kit.
* **I/O Bank Configuration:** The Icicle Kit's 40-pin connector routes to **Bank 1 and Bank 9**, configured for standard **3.3V LVCMOS** logic levels. The ADC's synchronous serial interface (SPI) or 8-bit parallel bus communicates directly with custom deserialization logic in the FPGA fabric.

---

### 3.2 PolarFire FPGA RTL Acceleration Pipeline

The FPGA fabric executes the continuous, compute-intensive DSP pipelines required by IEC 61000-4-30 Class A:

#### A. Zero-Crossing Detector & Digital Phase-Locked Loop (DPLL)
* Tracks the fundamental mains frequency ($50\text{ Hz} \pm 5\text{ Hz}$ or $60\text{ Hz} \pm 5\text{ Hz}$).
* Generates synchronized integer-sample reference pulses for cycle aggregation and phase angle calculation, maintaining exact synchronization even during heavily distorted waveform conditions.

#### B. Sliding Half-Cycle RMS Engine ($U_{rms(1/2)}$ and $I_{rms(1/2)}$)
Per IEC 61000-4-30 Section 5.1:
$$U_{rms(1/2)}[n] = \sqrt{\frac{1}{N_{half}} \sum_{k=0}^{N_{half}-1} v[n - k]^2}$$
* Rather than waiting for a full cycle or half-cycle to finish before outputting a value, the FPGA implements a **sliding window accumulator**:
  $$\text{Sum}[n] = \text{Sum}[n-1] + v[n]^2 - v[n - N_{half}]^2$$
* Every incoming sample updates the half-cycle RMS value. The square-root operation is executed using a pipelined CORDIC engine in vectoring mode.
* This allows PowerSentry-DC to detect voltage sags and swells within **less than 10 milliseconds** of occurrence.

#### C. ITIC (CBEMA) / SEMI-F47 Tolerance Mask Comparator
* Continuously evaluates instantaneous $U_{rms(1/2)}$ against programmed piece-wise linear tolerance curves:
  * Normal Operating Region (87% to 110% of nominal)
  * Sag Warning Region (70% to 87%)
  * Server Dropout / Trip Region (< 70% for > 20 ms)
  * Transient Overvoltage Swell Region (> 120%)
* When an excursion enters the prohibited region, the hardware comparator immediately latches the event timestamp and triggers an interrupt to the real-time RISC-V core.

#### D. Pipelined 1024-Point FFT Engine (Harmonics & Power Flow)
* Processes 10-cycle rectangular observation windows (200 ms at 50 Hz, 2048 samples grouped into consecutive 1024-point blocks).
* Computes magnitude and phase for harmonics from the fundamental ($h=1$) through the **63rd order** ($h=63$, 3150 Hz).
* Calculates:
  * Total Harmonic Distortion:
    $$\text{THD-V} = \frac{\sqrt{\sum_{h=2}^{63} V_h^2}}{V_1}, \quad \text{THD-I} = \frac{\sqrt{\sum_{h=2}^{63} I_h^2}}{I_1}$$
  * Triplen Harmonic Summation: Monitors additive zero-sequence currents ($3^{rd}, 9^{th}, 15^{th}, \dots$).
  * Dynamic K-Factor: Calculates transformer thermal stress coefficients in real time.
  * Directional Harmonic Power: Computes $P_h = V_h \cdot I_h \cdot \cos(\theta_h - \phi_h)$. Positive power indicates utility-to-load flow; negative power proves load-to-grid harmonic injection, definitively identifying rogue server racks.

#### E. Circular Pre/Post Trigger LSRAM Oscillogram Buffer
* Continuous ring buffer storing the latest 100 cycles of raw 16-bit 8-channel waveform samples inside PolarFire Large SRAM (LSRAM).
* When triggered by an ITIC violation or neutral current spike, the buffer freezes 20 cycles of pre-fault and 80 cycles of post-fault data, preventing overwrites while the AXI DMA engine transfers the oscillogram to system RAM for forensic export.

#### F. On-Chip Hardware-in-the-Loop (HIL) Test Playback Engine
* A built-in synthesizer ROM storing IEEE COMTRADE and PQDIF fault recordings (real data center voltage sags, capacitor switching spikes, and triplen harmonic current surges).
* MUXed with the physical ADC input and controlled via Icicle Kit push-buttons (SW1–SW4) to enable **100% realistic, safe benchtop demonstrations without requiring high-voltage equipment**.

---

### 3.3 RISC-V Microprocessor Subsystem (MSS) Asymmetric Multiprocessing (AMP)

The PolarFire SoC integrates a coherent 5-core 64-bit RISC-V processor cluster. PowerSentry-DC partitions these cores into dedicated functional domains using Asymmetric Multiprocessing (AMP):

```
+-----------------------------------------------------------------------------------+
|                     PolarFire SoC RISC-V MSS Cluster (600 MHz)                     |
+-------------------+--------------------+------------------------------------------+
|  Core 0 (E51)     |  Core 1 (U54)      |  Cores 2, 3, 4 (U54 Cluster)             |
|  Monitor & Power  |  Hard Real-Time    |  Embedded Linux OS                       |
+-------------------+--------------------+------------------------------------------+
| • System boot     | • FreeRTOS Kernel  | • Linux Kernel 6.x (Yocto/Debian)        |
| • Watchdog timers | • Sub-10µs ISR     | • NGINX Web Server + WebSocket Streamer  |
| • PAC1934 I2C     | • Modbus-TCP Server| • SQLite PQ Event / Trend Database       |
|   Telemetry       | • ITIC Event Logger| • MQTT Cloud Broker Gateway              |
| • Security config | • PTP / IEEE 1588  | • Real-time HTML5 Phasor & FFT Visualizer|
+-------------------+--------------------+------------------------------------------+
```

1. **Core 0 (Hart 0 - E51 Monitor Core):**
   * Acts as the primary system bootloader and supervisor.
   * Interfaces over I2C to the Icicle Kit's onboard **PAC1934** 4-channel power monitoring IC, tracking the board's own rail voltages and power dissipation to showcase PolarFire's low-power efficiency.
2. **Core 1 (Hart 1 - U54 Real-Time Core running FreeRTOS):**
   * Configured in real-time deterministic mode with private L1 cache.
   * Servicing FPGA hardware interrupts: responds to ITIC curve violations and neutral overcurrent alarms within **< 10 microseconds**.
   * Runs an industrial **Modbus-TCP server** over Gigabit Ethernet, providing instantaneous registers to Building Management Systems (BMS) and PLC automation.
3. **Cores 2, 3, and 4 (Harts 2–4 - U54 Linux Cluster):**
   * Boot an optimized embedded Linux distribution with SMP.
   * **Web Dashboard:** An embedded, responsive HTML5 dashboard powered by lightweight NGINX and WebSockets. Displays live 3-phase phasor diagrams, real-time harmonic bar graphs (1st to 63rd order), dynamic ITIC voltage tolerance plots, and neutral current alerts.
   * **Data Storage & Telemetry:** Logs Class A compliant 10-minute statistical aggregates and transient oscillograms in SQLite, while publishing JSON telemetry to cloud dashboards (AWS IoT / Azure IoT / ThingsBoard) via MQTT.

---

## 4. Hardware Resource Budget & Feasibility Analysis

The PolarFire SoC Icicle Kit features the **MPFS250T-FCVG484E** device. The table below details the estimated resource consumption for PowerSentry-DC against the kit's total capacity:

| Resource Type | Available on MPFS250T | Estimated Required for PowerSentry-DC | Utilization % | Feasibility Assessment |
| :--- | :---: | :---: | :---: | :--- |
| **Logic Elements (4-LUT + DFF)** | **254,000** | ~16,500 | **6.5%** | **Extremely Safe.** Massive headroom for future edge-AI models. |
| **Math Blocks (18x18 Multipliers)** | **784** | ~56 | **7.1%** | **Abundant.** Sliding squaring and FFT butterflies execute concurrently. |
| **LSRAM Blocks (20 Kbit each)** | **812 (16.2 Mb)** | ~40 (~800 Kb) | **4.9%** | Circular oscillograms and FFT ping-pong buffers fit entirely on-chip. |
| **uSRAM Blocks (64-bit)** | **1,296 (83 Kb)** | ~64 | **4.9%** | Used for sliding accumulator FIFO delay lines. |
| **RISC-V Application Cores** | **4x U54 @ 600 MHz** | 1 Core FreeRTOS + 3 Cores Linux | **100% Balanced** | Perfect heterogeneous AMP partitioning. |
| **Embedded System RAM** | **2 GB LPDDR4** | ~512 MB OS + Buffers | **25.0%** | Ample bandwidth for high-resolution waveform storage. |
| **High-Speed Networking** | **Dual Gigabit Ethernet** | 1 Port Active (VSC8662 PHY) | **50.0%** | Native Modbus-TCP and HTTP streaming. |

> **Conclusion on Feasibility:** With logic and DSP resource utilization well below 10%, the proposed design is exceptionally safe, free from timing closure bottlenecks, and easily synthesizable within the contest timeframe.

---

## 5. Testing & Verification Methodology (Without Live Data Centers)

To ensure rigorous validation and high visual impact for the demonstration video without requiring access to hazardous high-voltage facilities, PowerSentry-DC employs a **four-tier verification strategy**:

### Tier 1: Mathematical Golden Model vs. FPGA Simulation
* A comprehensive reference test harness implemented in **Python (NumPy / SciPy)** executing the exact mathematical equations of IEC 61000-4-30 Class A and IEEE 519.
* Identical synthetic test vectors are applied to both the Python model and the Libero ModelSim/Questa RTL simulation.
* **Pass Criterion:** FPGA half-cycle RMS and FFT harmonic magnitudes match the double-precision floating-point model within **< 0.1% error**, exceeding Class A certification thresholds.

### Tier 2: On-Chip Hardware-in-the-Loop (HIL) Playback
* Pre-recorded COMTRADE data center power quality records (captured during real grid events, transformer inrush, and server rack dropouts) are compiled into FPGA block ROM.
* Icicle Kit push-buttons trigger specific fault injection scenarios:
  * **Scenario A:** Standard nominal 50 Hz balanced grid.
  * **Scenario B:** 7-cycle voltage sag down to 55% nominal (tripping the ITIC curve mask).
  * **Scenario C:** High triplen harmonic injection (neutral current surging to 150% of phase current).
  * **Scenario D:** Microsecond capacitor switching transient.
* The video demonstration clearly shows the system detecting the fault, latching the event, illuminating board status LEDs, and updating the web dashboard in real time.

### Tier 3: Safe Low-Voltage Physical Benchtop Testbench
* An off-the-shelf **AD7606 8-channel ADC breakout board** connected to the Icicle Kit's 40-pin header.
* Driven by a safe **12V AC step-down transformer** and dual-channel arbitrary function generator (0–3.3V safe analog range).
* A miniature non-linear load (diode bridge rectifier + resistive/capacitive load and phase-cut dimmer) generates real harmonic currents and demonstrates physical neutral current summation on a benchtop oscilloscope and PowerSentry-DC dashboard simultaneously.

### Tier 4: End-to-End Network & SCADA Telemetry
* Verification of industrial Modbus-TCP register polling via QModMaster / Python scripts.
* Live streaming of real-time oscillograms over WebSockets to modern web browsers.

---

## 6. Risk Analysis & Mitigation Matrix

| Potential Risk | Severity | Likelihood | Mitigation Strategy |
| :--- | :---: | :---: | :--- |
| **Timing Closure on 1024-pt FFT** | Medium | Low | Pipelined radix-2/radix-4 architecture with internal registers; target clock is only 50–100 MHz, well below PolarFire's 300+ MHz maximum fabric speed. |
| **Linux-FreeRTOS Inter-Processor Communication (IPC)** | Medium | Low | Utilize PolarFire SoC hardware Core-to-Core Mailbox interrupts and shared LPDDR4 memory blocks with OpenAMP standard protocols. |
| **ADC Interface Signal Integrity** | Low | Low | Keep header jumper wires short (< 10 cm); operate AD7606 SPI bus at conservative clock speeds (10–16 MHz), which provides over $10\times$ the bandwidth required for 10.24 kS/s. |
| **Development Kit Shipment Delays** | Medium | Medium | Complete Python golden model and full RTL testbenches in simulation prior to kit delivery; all Verilog code is fully synthesizable and testable in ModelSim ahead of time. |

---

## 7. Milestone Schedule & Execution Timeline

```
+-----------------------------------------------------------------------------------------+
| Milestone Schedule: PolarFire FPGA Design Contest (Aug 2026 - May 2027)                 |
+-----------------------------------------------------------------------------------------+
  Aug - Oct 2026   | Phase 0: Proposal Submission & Python Golden Model Development
  Nov - Dec 2026   | Phase 1: RTL Design (ADC Controller, DPLL, Sliding RMS, ITIC Engine)
  Jan 2027         | Phase 2: Pipelined 1024-pt FFT, Harmonic Analyzer & LSRAM Buffers
  Feb 2027         | Phase 3: RISC-V MSS AMP Setup (FreeRTOS Core 1 + Embedded Linux Web GUI)
  Mar 2027         | Phase 4: Benchtop HIL Integration, Video Demonstration & Final Report
  May 2027         | Phase 5: Winner Announcements
+-----------------------------------------------------------------------------------------+
```

* **Milestone 1 (Oct 3, 2026):** Proposal submission via official competition portal and public GitHub repository launch.
* **Milestone 2 (Nov 30, 2026):** Complete Python algorithmic verification; Libero SoC project scaffolded with simulated AD7606 SPI driver and sliding half-cycle RMS engine.
* **Milestone 3 (Dec 31, 2026):** Functional RTL simulation of ITIC/SEMI-F47 curve comparator and circular oscillogram buffer.
* **Milestone 4 (Jan 31, 2027):** 1024-point FFT harmonic decomposition verified in ModelSim; THD and K-factor registers integrated via AXI4-Lite.
* **Milestone 5 (Feb 28, 2027):** PolarFire SoC Icicle Kit integration: FreeRTOS ISR responding to hardware interrupts, Linux web server streaming live metrics over Gigabit Ethernet.
* **Milestone 6 (Mar 27, 2027):** Final submission: comprehensive 10-page technical paper, full GitHub repository release (MIT License), and a 3-to-5 minute high-definition demonstration video.

---

## 8. Bill of Materials (BOM) & Prototype Economics

| Component | Part / Description | Source / Vendor | Estimated Cost (USD) |
| :--- | :--- | :--- | :---: |
| **FPGA Platform** | PolarFire SoC Icicle Kit (`MPFS250T`) | Microchip / Contest Provided | \$0 (Provided) |
| **Analog ADC Board** | AD7606 8-Channel 16-Bit 200 kSPS Breakout | Analog Devices / Waveshare | ~\$12 – \$18 |
| **Interconnect** | 40-Pin Ribbon Cable to J26/J27 Header | Standard Electronic Supply | ~\$3 |
| **Safe AC Test Source**| 230V to 12V AC Step-Down Safety Transformer | Standard Electronic Supply | ~\$8 – \$12 |
| **Benchtop Load** | Diode Bridge Rectifier + Resistors / Dimmers | Lab Components | ~\$5 |
| **Networking** | Standard Cat6 Ethernet Patch Cable | Standard Electronic Supply | ~\$2 |
| **Total Prototype Hardware Cost (Excluding Kit):** | | | **~ \$30 – \$40** |

---

## 9. Alignment with Contest Scoring Criteria

1. **Technical Feasibility (35%):**
   * Conservative resource utilization (< 10% LEs, < 10% Math blocks) guarantees feasibility on the MPFS250T.
   * Utilizes standard, validated Microchip IP (AXI interconnect, DDR controllers, RISC-V MSS).
   * Fully verifiable on a benchtop using on-chip HIL simulation and low-cost ADC modules.
2. **Innovation & Creativity (25%):**
   * Eliminates the traditional "blind spot" of data center metering through sub-cycle sliding RMS and instantaneous ITIC curve tracking.
   * Directly solves the reverse triplen harmonic problem and transformer overheating via real-time neutral current summing and dynamic K-factor synthesis.
   * Implements true Asymmetric Multiprocessing (AMP) across PolarFire's 5-core RISC-V cluster.
3. **Problem Statement & Solution Clarity (20%):**
   * Solves an urgent, multi-million-dollar industry pain point: high-density AI data center electrical downtime and fire hazards.
   * Standard-driven methodology anchored in internationally recognized benchmarks (IEC 61000-4-30 Class A, ITIC, SEMI-F47, IEEE 519).
4. **Potential Impact (20%):**
   * Directly applicable to every modern data center, semiconductor manufacturing facility, and industrial microgrid.
   * Highly scalable, reproducible, and open for commercialization as an embedded edge PDU monitoring sentinel.
