# PowerSentry-DC ⚡🛡️
### Real-Time IEC 61000-4-30 Class A Power Quality Analyzer & ITIC Ride-Through Sentinel for High-Density Data Centers

[![Microchip PolarFire SoC](https://img.shields.io/badge/Microchip-PolarFire%20SoC%20Icicle%20Kit-blue.svg)](https://www.microchip.com/en-us/development-tool/mpfs-icicle-kit)
[![Contest Track](https://img.shields.io/badge/Track%202-Connected%20Real--Time%20Systems-green.svg)](https://www.microchip.com/en-us/campaigns/polarfire-fpga-design-contest)
[![Target Silicon](https://img.shields.io/badge/FPGA-MPFS250T--FCVG484E-orange.svg)](https://www.microchip.com/en-us/products/fpgas-and-plds/system-on-chip-fpgas/polarfire-soc-fpgas)
[![Standard](https://img.shields.io/badge/Standard-IEC%2061000--4--30%20Class%20A-red.svg)](https://www.iec.ch)
[![Processor](https://img.shields.io/badge/ISA-64--bit%20RISC--V%20(5--Core%20AMP)-purple.svg)](https://riscv.org)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

---

## 🏛️ System Architecture

![PowerSentry-DC Architecture Block Diagram](docs/SYSTEM_BLOCK_DIAGRAM.png)

> 📄 **Official Submission Document:** Download the publication-grade [System Block Diagram (PDF)](docs/SYSTEM_BLOCK_DIAGRAM.pdf).

---

## 📌 Project Overview

As AI/ML and HPC clusters push data center rack densities past 40–100 kW, electrical infrastructure faces two under-monitored risks. Standard Multi-Function Meters average voltage over 1-second to 10-minute windows, making them blind to brief voltage sags that breach ITIC/SEMI-F47 tolerance curves — these events deplete server power-supply holdup capacitors, triggering simultaneous multi-rack reboots with no forensic record of the cause. Separately, non-linear server power supplies inject triplen harmonics (3rd, 9th, 15th) that sum additively in the neutral conductor of 4-wire distribution systems rather than canceling, often reaching 140–170% of phase current — creating overheating and fire risk invisible to standard phase-only breaker monitoring.

PowerSentry-DC addresses both gaps on the Microchip PolarFire SoC Icicle Kit (MPFS250T). An 8-channel simultaneous-sampling AD7606 ADC feeds a deterministic FPGA DSP pipeline that recalculates sliding half-cycle RMS on every sample (10.24 kS/s), comparing live voltage against ITIC/SEMI-F47 curves and triggering a sub-10-microsecond hardware interrupt for protective shedding or UPS transfer before servers crash. A parallel 1024-point FFT pipeline computes harmonics to the 63rd order, true THD, and dynamic transformer K-factor, while directional harmonic power flow distinguishes utility-side pollution from internally generated server harmonics. Pre/post-fault waveforms are captured via on-chip LSRAM and DMA-streamed to LPDDR4 for forensic review.

A RISC-V AMP subsystem splits work cleanly: one FreeRTOS core handles deterministic event logging and Modbus-TCP for SCADA/PLC integration, while Linux cores host a web dashboard and MQTT gateway. Estimated FPGA resource utilization is under 10% across logic and DSP blocks, indicating strong feasibility within the contest timeline, with total additional prototype hardware cost under $40.

---

## 💡 Innovation & Expected Impact

Commercial Class A power-quality analyzers rely on sequential microcontroller or multi-chip DSP+MCU architectures that struggle to sustain simultaneous multi-channel sampling, sliding RMS, FFT decomposition, and continuous oscillography without buffer overruns — and typically cost thousands of dollars per monitoring point, limiting deployment to a few shared panels per facility.

PowerSentry-DC's innovation is architectural: implementing the full DSP pipeline as deterministic, zero-jitter hardware logic on PolarFire's FPGA fabric, rather than software on a sequential processor, achieves hard real-time, sub-10-microsecond fault response at an embedded, low-cost footprint (under $40 in additional hardware beyond the kit). This shifts power-quality monitoring from a handful of expensive, centrally located instruments toward dense, per-rack or per-PDU deployment.

A key differentiator is directional harmonic active-power-flow calculation, which distinguishes utility-grid-origin pollution from internally generated server harmonics — letting facilities teams pinpoint root cause rather than merely detect symptoms, a diagnostic capability standard panel meters lack. Validation combines a Python/NumPy golden model of the IEC 61000-4-30 formulas (targeting agreement within 0.1% of the reference), recorded real-world fault playback (COMTRADE/PQDIF), and physical low-voltage benchtop testing — demonstrating rigor without requiring live high-voltage facility access.

Potential impact spans preventing costly multi-rack reboot events, reducing neutral-conductor fire risk, extending transformer life through K-factor-aware load management, and enabling facility-wide power-quality visibility at a fraction of traditional analyzer cost — directly scalable to every modern high-density data center, semiconductor fab, and industrial microgrid.

---

## 📊 Hardware Resource Utilization (MPFS250T)

Targeted for the **Microchip PolarFire SoC Icicle Kit (`MPFS250T-FCVG484E`)**:

| Resource Type | Available on Device | Used by PowerSentry-DC | Utilization % | Feasibility Status |
| :--- | :---: | :---: | :---: | :---: |
| **Logic Elements (4-LUT + DFF)** | **254,000** | ~16,500 | **6.5%** | ✅ Massive Headroom |
| **Math Blocks (18x18 Multipliers)** | **784** | ~56 | **7.1%** | ✅ Concurrency Guaranteed |
| **LSRAM Blocks (20 Kbit each)** | **812 (16.2 Mb)** | ~40 (~800 Kb) | **4.9%** | ✅ On-Chip Oscillograms |
| **uSRAM Blocks (64-bit)** | **1,296 (83 Kb)** | ~64 | **4.9%** | ✅ FIFO Delay Pipelines |
| **64-bit RISC-V Application Cores** | **4x U54 @ 600 MHz** | 1 FreeRTOS + 3 Linux | **100%** | ✅ Balanced AMP Profile |
| **Onboard High-Speed Memory** | **2 GB LPDDR4** | ~512 MB OS / Buffers | **25.0%** | ✅ Ample High-Res Storage |
| **On-board Diagnostics** | **PAC1934 (4-Ch I2C)** | Native Icicle Bus | **Native** | ✅ Kit Power Telemetry |

---

## 🧪 Verification & Testing Strategy

Judges and evaluators can verify PowerSentry-DC completely within a laboratory or desktop environment without requiring access to live high-voltage data centers:

1. **Python Golden Model:** Double-precision reference model validating IEC 61000-4-30 formulas and ITIC boundaries against ModelSim RTL simulations targeting < 0.1% error.
2. **On-Chip HIL Playback:** Pre-stored real data center IEEE COMTRADE disturbance records compiled into FPGA block ROM. Board push-buttons simulate 5-cycle sags, capacitor switching spikes, and neutral current surges on demand.
3. **Safe Low-Voltage Hardware Testbench:** An off-the-shelf AD7606 8-channel ADC module (~$15) connects to the 40-pin header, driven by a safe 12V AC step-down transformer and miniature diode-bridge non-linear load.
4. **End-to-End Live Dashboard:** Dual Gigabit Ethernet streams real-time phasors, harmonic bars, and ITIC curve status via WebSockets.

---

## 📅 Project Milestones (Contest Timeline)

* **Phase 0 (Oct 3, 2026):** Proposal submission via official competition portal & public repository release.
* **Phase 1 (Dec 2026):** Libero SoC project scaffolding, AD7606 SPI interface controller, and sliding half-cycle RMS engine.
* **Phase 2 (Jan 2027):** Pipelined 1024-pt FFT harmonic decomposition (up to 63rd order) and circular LSRAM oscillogram buffer.
* **Phase 3 (Feb 2027):** PolarFire SoC Icicle Kit AMP integration: FreeRTOS sub-10µs ISR, Linux web dashboard, and Modbus-TCP telemetry.
* **Phase 4 (Mar 27, 2027):** Final submission: comprehensive 10-page documentation, full source code release, and 3–5 minute high-definition demonstration video.
* **Phase 5 (May 15, 2027):** Winner announcements.

---

## 📝 Proposal Documentation & Contest Details

* **Organizers:** Microchip Technology Inc. & DigiKey
* **Competition:** PolarFire® FPGA Design Contest 2026–27
* **Track:** Track 2: Connected Real-Time Systems
* **Target Hardware:** PolarFire® SoC Icicle Kit (`MPFS-ICICLE-KIT-ES` / `MPFS250T`)
* **Supplemental Proposal Document:** See [**`docs/PROPOSAL.md`**](docs/PROPOSAL.md) for the complete formal engineering proposal.
* **Architecture Diagram:** See [**`docs/SYSTEM_BLOCK_DIAGRAM.pdf`**](docs/SYSTEM_BLOCK_DIAGRAM.pdf).

---

## 📜 License
This project is released under the [MIT License](LICENSE).
