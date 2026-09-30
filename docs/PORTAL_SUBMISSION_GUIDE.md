# Microchip PolarFire FPGA Design Contest 2026–27
## Official Portal Submission Guide & Quick Copy-Paste

> **Contest Link:** [Microchip PolarFire FPGA Design Contest](https://www.microchip.com/en-us/campaigns/polarfire-fpga-design-contest)  
> **Registration & Proposal Deadline:** **October 3, 2026 at 11:59 PM PDT**  
> **Project Name:** **PowerSentry-DC**  
> **Selected Track:** **Track 2: Connected Real-Time Systems (PolarFire® SoC Icicle Kit)**  

---

### Field 1: Development Platform (Competition Track)
* **Selection:** `Track 2: Connected Real-Time Systems (PolarFire SoC Icicle Kit)`

---

### Field 2: Project Overview *(Word Limit: Maximum 300 Words)*
> **Word count of text below:** **286 words**

Modern hyperscale and enterprise data centers face severe operational vulnerabilities stemming from power quality anomalies that conventional Multi-Function Meters (MFMs) fail to detect. While MFMs aggregate metrics over 1-second to 10-minute averaging windows, high-density server racks crash during sub-cycle transients and 5-to-10 cycle voltage sags. Simultaneously, thousands of non-linear Server Power Supply Units (PSUs) inject severe 3rd, 9th, and 15th (triplen) harmonic currents that flow backwards from loads toward distribution transformers. Because triplen harmonics sum additively in the neutral conductor rather than canceling, neutral conductors and transformer coils experience extreme thermal stress, insulation breakdown, and severe fire hazards—even when phase currents appear balanced and well within rated limits.

**PowerSentry-DC** is an FPGA-accelerated, deterministic Power Quality (PQ) analyzer and ITIC/SEMI-F47 ride-through sentinel engineered on the Microchip PolarFire SoC Icicle Kit (MPFS250T). The system interfaces to an 8-channel simultaneous-sampling ADC (AD7606) via the 40-pin Raspberry Pi expansion header to monitor 3-phase voltages, currents, neutral current, and earth leakage.

Within the PolarFire FPGA fabric, dedicated RTL engines execute sliding half-cycle RMS calculations ($U_{rms(1/2)}$, $I_{rms(1/2)}$) compliant with IEC 61000-4-30 Class A, an instantaneous ITIC/SEMI-F47 curve mask comparator, and a pipelined 1024-point FFT computing harmonic spectra up to the 63rd order, THD, and dynamic transformer K-Factor. When voltage sags breach server ride-through boundaries or neutral currents surge, the FPGA asserts a sub-10-microsecond hardware interrupt to a deterministic FreeRTOS RISC-V core while capturing 100 cycles of pre/post-fault oscillography into LSRAM. Concurrent 64-bit Linux RISC-V cores host an interactive web dashboard, log events to an onboard database, and stream telemetry over Dual Gigabit Ethernet via Modbus-TCP and MQTT.

PowerSentry-DC delivers legally defensible Class A power event forensics, safeguarding data center reliability and mitigating catastrophic fire hazards.

---

### Field 3: Innovation & Expected Impact *(Word Limit: Maximum 250 Words)*
> **Word count of text below:** **238 words**

**Innovation & Key Differentiators:**  
PowerSentry-DC overcomes the latency, resolution, and blindness limitations of conventional microprocessor-based metering through a tightly integrated FPGA/RISC-V Asymmetric Multiprocessing (AMP) architecture:
1. **Zero-Blindness Sub-Cycle Detection:** Conventional meters miss 5–10 cycle dropouts; PowerSentry-DC’s pipelined hardware RMS engine slides on a single-sample basis, detecting ITIC curve violations in under 10 milliseconds.
2. **Reverse Triplen Harmonic & K-Factor Sentinel:** Rather than merely reporting total harmonic distortion (THD), the FPGA computes directional harmonic active power and real-time neutral current summation, pinpointing whether harmonic degradation originates from server PSUs or the upstream grid.
3. **Deterministic Heterogeneous AMP Partitioning:** Time-critical fault capture and sub-10µs protection interrupts are handled by dedicated FPGA logic and a hard real-time FreeRTOS RISC-V core (U54), while non-real-time tasks (NGINX web server, WebSocket oscillograms, cloud MQTT, and Class A PQDIF export) execute across Linux cores without introducing pipeline jitter.
4. **Ultra-Low Power Profile:** Leveraging PolarFire’s non-volatile flash architecture, the solution delivers high-throughput DSP performance at a fraction of the thermal footprint of SRAM-based FPGAs, monitored natively via the Icicle Kit's onboard PAC1934 IC.

**Expected Impact:**  
With global data center power consumption surging from AI computing workloads, unplanned electrical outages cost operators upwards of \$10,000 per minute. PowerSentry-DC provides an accessible, certifiable Class A sentinel that eliminates server crashes, prevents neutral conductor electrical fires, and accelerates utility tariff dispute resolution across critical power infrastructure.

---

### Field 4: Shared Drive / Repository Link
* **Drive Platform:** GitHub *(Allowed per Contest Rules Section 6)*
* **URL:** `https://github.com/<YOUR_GITHUB_USERNAME>/PowerSentry-DC` *(Make sure this repo is set to **Public** before submitting)*
* **PDF Block Diagram File:** Ensure `docs/SYSTEM_BLOCK_DIAGRAM.pdf` is present and accessible in the root/docs of your public repository.
