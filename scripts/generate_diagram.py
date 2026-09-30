import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_system_block_diagram(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Background styling
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    
    # Title & Header
    ax.text(8.0, 10.5, "PowerSentry-DC: System Architecture Block Diagram", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#0F172A', family='sans-serif')
    ax.text(8.0, 10.15, "IEC 61000-4-30 Class A Power Quality Analyzer & ITIC Ride-Through Sentinel | Microchip PolarFire SoC Icicle Kit (MPFS250T)", 
            fontsize=10.5, ha='center', va='center', color='#475569', family='sans-serif')
    
    # SECTION 1: SENSOR FRONT-END & ACQUISITION (Left)
    rect_sensor = patches.FancyBboxPatch((0.5, 3.2), 3.2, 6.3, boxstyle="round,pad=0.15,rounding_size=0.15",
                                        facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=2)
    ax.add_patch(rect_sensor)
    ax.text(2.1, 9.2, "ANALOG FRONT-END (AFE)", fontsize=11, fontweight='bold', ha='center', color='#1E40AF')
    
    # 3-Phase + N + E Inputs
    rect_inputs = patches.FancyBboxPatch((0.7, 7.5), 2.8, 1.4, boxstyle="round,pad=0.1",
                                         facecolor='#DBEAFE', edgecolor='#60A5FA', linewidth=1.2)
    ax.add_patch(rect_inputs)
    ax.text(2.1, 8.45, "3-Phase Power Distribution", fontsize=9.5, fontweight='bold', ha='center', color='#1E3A8A')
    ax.text(2.1, 8.0, "3x Voltage (Va, Vb, Vc)\n3x Phase Current (Ia, Ib, Ic)\nNeutral (In) & Earth/GND (Ie)", 
            fontsize=8, ha='center', color='#1E3A8A')
    
    # Signal Conditioning & Attenuation
    rect_cond = patches.FancyBboxPatch((0.7, 5.7), 2.8, 1.4, boxstyle="round,pad=0.1",
                                       facecolor='#FFFFFF', edgecolor='#93C5FD', linewidth=1)
    ax.add_patch(rect_cond)
    ax.text(2.1, 6.65, "Signal Conditioning", fontsize=9.5, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(2.1, 6.2, "PT Potential Dividers\nCTs / Shunt Resistors\nAnti-Aliasing Filter (Butterworth)", 
            fontsize=8, ha='center', color='#334155')
    
    # AD7606 Module
    rect_adc = patches.FancyBboxPatch((0.7, 3.5), 2.8, 1.8, boxstyle="round,pad=0.1",
                                      facecolor='#DBEAFE', edgecolor='#2563EB', linewidth=1.5)
    ax.add_patch(rect_adc)
    ax.text(2.1, 4.95, "AD7606 ADC Subsystem", fontsize=10, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(2.1, 4.4, "8-Channel Simultaneous Sampling\n16-Bit SAR Resolution @ 10.24 kS/s\n(204.8 samples/cycle @ 50 Hz)\nTrue Bipolar Inputs (±5V / ±10V)", 
            fontsize=7.8, ha='center', color='#1E3A8A')
    ax.text(2.1, 3.7, "Plugs via 40-Pin RPi Header (3.3V)", fontsize=8, fontweight='bold', ha='center', color='#B45309')

    # SECTION 2: POLARFIRE SOC FPGA FABRIC (Center)
    rect_fpga = patches.FancyBboxPatch((4.2, 0.6), 6.5, 8.9, boxstyle="round,pad=0.2,rounding_size=0.2",
                                       facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=2.5)
    ax.add_patch(rect_fpga)
    ax.text(7.45, 9.2, "POLARFIRE SoC FPGA FABRIC (MPFS250T)", fontsize=12, fontweight='bold', ha='center', color='#166534')
    ax.text(7.45, 8.9, "254K LEs | 784 Math Blocks | Low Static Power (<1W fabric)", fontsize=8.5, ha='center', color='#15803D')
    
    # Sub-block 1: ADC Controller & PLL
    rect_adcc = patches.FancyBboxPatch((4.5, 7.4), 2.8, 1.25, boxstyle="round,pad=0.08",
                                       facecolor='#DCFCE7', edgecolor='#4ADE80', linewidth=1.2)
    ax.add_patch(rect_adcc)
    ax.text(5.9, 8.25, "ADC Master Interface", fontsize=9.5, fontweight='bold', ha='center', color='#14532D')
    ax.text(5.9, 7.8, "High-Speed SPI / 8-bit Parallel\nSynchronous 8-Ch Data Deserializer", fontsize=8, ha='center', color='#166534')

    rect_pll = patches.FancyBboxPatch((7.6, 7.4), 2.8, 1.25, boxstyle="round,pad=0.08",
                                      facecolor='#DCFCE7', edgecolor='#4ADE80', linewidth=1.2)
    ax.add_patch(rect_pll)
    ax.text(9.0, 8.25, "Zero-Crossing & DPLL", fontsize=9.5, fontweight='bold', ha='center', color='#14532D')
    ax.text(9.0, 7.8, "Synchronized to Fundamental\nFrequency Lock (50 Hz ±5 Hz)", fontsize=8, ha='center', color='#166534')

    # Sub-block 2: Sliding Half-Cycle RMS Engine
    rect_rms = patches.FancyBboxPatch((4.5, 5.5), 5.9, 1.6, boxstyle="round,pad=0.1",
                                      facecolor='#FFFFFF', edgecolor='#22C55E', linewidth=1.5)
    ax.add_patch(rect_rms)
    ax.text(7.45, 6.75, "Sliding Half-Cycle RMS Engine: Urms(1/2) & Irms(1/2)", fontsize=10, fontweight='bold', ha='center', color='#15803D')
    ax.text(7.45, 6.25, "IEC 61000-4-30 Class A Compliant (Overlapping 10ms window, 1-sample slide)\nHardware Square-Accumulate-SquareRoot Pipeline | 8 Concurrent Channels\nInstantaneous Sag / Swell / Interruption Detection within 10 milliseconds", 
            fontsize=7.8, ha='center', color='#334155')
    ax.text(7.45, 5.75, "Estimated DSP Usage: 16 Math Blocks (2.0%) | 100% Deterministic", 
            fontsize=7.5, fontweight='bold', ha='center', color='#15803D')

    # Sub-block 3: ITIC / SEMI-F47 Mask Comparator
    rect_itic = patches.FancyBboxPatch((4.5, 3.65), 2.8, 1.6, boxstyle="round,pad=0.08",
                                       facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
    ax.add_patch(rect_itic)
    ax.text(5.9, 4.9, "ITIC / SEMI-F47 Curve Engine", fontsize=9.5, fontweight='bold', ha='center', color='#92400E')
    ax.text(5.9, 4.3, "Real-time voltage vs. duration mask\nDetects 5-10 cycle server dropouts\nTriggers sub-10µs Hardware IRQ\nto FreeRTOS Core 1", 
            fontsize=7.8, ha='center', color='#78350F')

    # Sub-block 4: Pipelined 1024-pt FFT Engine
    rect_fft = patches.FancyBboxPatch((7.6, 3.65), 2.8, 1.6, boxstyle="round,pad=0.08",
                                      facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=1.5)
    ax.add_patch(rect_fft)
    ax.text(9.0, 4.9, "Pipelined 1024-pt FFT", fontsize=9.5, fontweight='bold', ha='center', color='#14532D')
    ax.text(9.0, 4.3, "Harmonic Spectrum (1st to 63rd)\nTHD-V, THD-I, Dynamic K-Factor\nNeutral Triplen Sum (3rd, 9th, 15th)\nReverse Power Flow Direction", 
            fontsize=7.8, ha='center', color='#166534')

    # Sub-block 5: Circular Oscillography Buffer & HIL Playback
    rect_buf = patches.FancyBboxPatch((4.5, 2.05), 2.8, 1.35, boxstyle="round,pad=0.08",
                                      facecolor='#FFFFFF', edgecolor='#86EFAC', linewidth=1.2)
    ax.add_patch(rect_buf)
    ax.text(5.9, 3.05, "Circular Waveform Buffer", fontsize=9, fontweight='bold', ha='center', color='#166534')
    ax.text(5.9, 2.6, "100-Cycle Fault Oscillography\nEmbedded LSRAM Ping-Pong Buffer\nPre & Post-Trigger Capture", 
            fontsize=7.5, ha='center', color='#334155')

    rect_hil = patches.FancyBboxPatch((7.6, 2.05), 2.8, 1.35, boxstyle="round,pad=0.08",
                                      facecolor='#EFF6FF', edgecolor='#60A5FA', linewidth=1.2)
    ax.add_patch(rect_hil)
    ax.text(9.0, 3.05, "On-Chip HIL Playback ROM", fontsize=9, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(9.0, 2.6, "COMTRADE Fault Synthesizer\nBenchtop Demo / No Live DC Needed\nPush-Button Fault Triggering", 
            fontsize=7.5, ha='center', color='#1E3A8A')

    # Sub-block 6: AXI Bus Interface
    rect_axi = patches.FancyBboxPatch((4.5, 0.85), 5.9, 0.95, boxstyle="round,pad=0.08",
                                      facecolor='#E2E8F0', edgecolor='#64748B', linewidth=1.2)
    ax.add_patch(rect_axi)
    ax.text(7.45, 1.45, "AXI4-Lite Slave & High-Throughput AXI DMA Engine", fontsize=9.5, fontweight='bold', ha='center', color='#1E293B')
    ax.text(7.45, 1.1, "Bidirectional Interconnect between FPGA DSP Pipeline & RISC-V Microprocessor Subsystem", 
            fontsize=7.8, ha='center', color='#475569')

    # SECTION 3: RISC-V MSS (Right)
    rect_mss = patches.FancyBboxPatch((11.1, 1.8), 4.4, 7.7, boxstyle="round,pad=0.2,rounding_size=0.2",
                                      facecolor='#FAF5FF', edgecolor='#9333EA', linewidth=2.5)
    ax.add_patch(rect_mss)
    ax.text(13.3, 9.2, "RISC-V MICROPROCESSOR SUBSYSTEM", fontsize=11, fontweight='bold', ha='center', color='#6B21A8')
    ax.text(13.3, 8.9, "5-Core Heterogeneous Cluster @ 600 MHz (AMP)", fontsize=8.5, ha='center', color='#7E22CE')

    # Core 0: E51 System Monitor
    rect_e51 = patches.FancyBboxPatch((11.3, 7.3), 4.0, 1.35, boxstyle="round,pad=0.08",
                                      facecolor='#F3E8FF', edgecolor='#C084FC', linewidth=1.2)
    ax.add_patch(rect_e51)
    ax.text(13.3, 8.25, "Core 0: E51 Monitor Core", fontsize=9.5, fontweight='bold', ha='center', color='#581C87')
    ax.text(13.3, 7.75, "System Boot, Watchdog, Clock Security\nPAC1934 I2C Power Monitor (Board Power Telemetry)", 
            fontsize=7.8, ha='center', color='#6B21A8')

    # Core 1: U54 FreeRTOS Real-Time
    rect_u54_rt = patches.FancyBboxPatch((11.3, 5.55), 4.0, 1.5, boxstyle="round,pad=0.08",
                                         facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.5)
    ax.add_patch(rect_u54_rt)
    ax.text(13.3, 6.7, "Core 1: U54 Real-Time Core (FreeRTOS)", fontsize=9.5, fontweight='bold', ha='center', color='#991B1B')
    ax.text(13.3, 6.15, "Hard Real-Time ISR Response (< 10 µs)\nITIC Curve Sag / Swell Event Logger\nModbus-TCP Server for SCADA / PLC\nHigh-Precision IEC Event Timestamping", 
            fontsize=7.8, ha='center', color='#7F1D1D')

    # Cores 2-4: U54 Linux Cluster
    rect_u54_lx = patches.FancyBboxPatch((11.3, 3.5), 4.0, 1.8, boxstyle="round,pad=0.08",
                                         facecolor='#FFFFFF', edgecolor='#A855F7', linewidth=1.5)
    ax.add_patch(rect_u54_lx)
    ax.text(13.3, 4.95, "Cores 2, 3, 4: U54 Cluster (Embedded Linux)", fontsize=9.5, fontweight='bold', ha='center', color='#581C87')
    ax.text(13.3, 4.35, "Full Yocto/Debian Linux Kernel 6.x\nInteractive Web Dashboard (NGINX + WebSockets)\nITIC / SEMI-F47 Tolerance Chart Generator\nMQTT / REST Cloud Gateway (DCIM Integration)\nSQLite Circular Event Database", 
            fontsize=7.6, ha='center', color='#334155')

    # Memory & Peripherals Box
    rect_periph = patches.FancyBboxPatch((11.3, 2.05), 4.0, 1.25, boxstyle="round,pad=0.08",
                                         facecolor='#F3E8FF', edgecolor='#D8B4FE', linewidth=1.2)
    ax.add_patch(rect_periph)
    ax.text(13.3, 2.95, "Storage & Memory Subsystem", fontsize=9, fontweight='bold', ha='center', color='#581C87')
    ax.text(13.3, 2.5, "2 GB LPDDR4 RAM (High-Res Buffering)\n16 GB eMMC / MicroSD (Long-term Trend Storage)", 
            fontsize=7.8, ha='center', color='#6B21A8')

    # SECTION 4: EXTERNAL CONNECTIVITY & CLOUD/DCIM (Bottom Right & Left)
    rect_io = patches.FancyBboxPatch((11.1, 0.4), 4.4, 1.15, boxstyle="round,pad=0.08",
                                     facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=1.5)
    ax.add_patch(rect_io)
    ax.text(13.3, 1.15, "EXTERNAL CONNECTIVITY & DCIM", fontsize=9.5, fontweight='bold', ha='center', color='#0369A1')
    ax.text(13.3, 0.75, "Dual Gigabit Ethernet RJ45 | USB-UART Console\nModbus-TCP / MQTT / HTTP / REST APIs", 
            fontsize=8, ha='center', color='#075985')

    # ARROWS & BUS CONNECTIONS
    # AFE -> ADC
    ax.annotate('', xy=(2.1, 5.7), xytext=(2.1, 7.5),
                arrowprops=dict(arrowstyle="-|>", color='#1E40AF', lw=2))
    ax.annotate('', xy=(2.1, 3.5), xytext=(2.1, 4.3),
                arrowprops=dict(arrowstyle="-|>", color='#1E40AF', lw=2))
    
    # ADC -> FPGA Header
    ax.annotate('', xy=(4.2, 4.4), xytext=(3.5, 4.4),
                arrowprops=dict(arrowstyle="-|>", color='#2563EB', lw=2.5))
    ax.text(3.85, 4.65, "40-Pin RPi\nSPI / GPIO", fontsize=7.5, fontweight='bold', ha='center', color='#2563EB')

    # Inside FPGA connections
    # ADC Controller -> DPLL
    ax.annotate('', xy=(7.6, 8.0), xytext=(7.3, 8.0),
                arrowprops=dict(arrowstyle="<|-|>", color='#16A34A', lw=1.5))
    
    # ADC Controller -> RMS
    ax.annotate('', xy=(5.9, 7.1), xytext=(5.9, 7.4),
                arrowprops=dict(arrowstyle="-|>", color='#16A34A', lw=2))
    
    # RMS -> ITIC & FFT
    ax.annotate('', xy=(5.9, 5.25), xytext=(5.9, 5.5),
                arrowprops=dict(arrowstyle="-|>", color='#D97706', lw=2))
    ax.annotate('', xy=(9.0, 5.25), xytext=(9.0, 5.5),
                arrowprops=dict(arrowstyle="-|>", color='#16A34A', lw=2))
    
    # ITIC / FFT -> Buffer & AXI
    ax.annotate('', xy=(5.9, 3.4), xytext=(5.9, 3.65),
                arrowprops=dict(arrowstyle="-|>", color='#16A34A', lw=1.5))
    ax.annotate('', xy=(7.45, 1.8), xytext=(7.45, 2.05),
                arrowprops=dict(arrowstyle="-|>", color='#16A34A', lw=2))
    
    # FPGA AXI <-> MSS Interconnect
    ax.annotate('', xy=(11.1, 1.3), xytext=(10.4, 1.3),
                arrowprops=dict(arrowstyle="<|-|>", color='#7C3AED', lw=3))
    ax.text(10.75, 1.55, "AXI4\nDMA/Lite", fontsize=7.5, fontweight='bold', ha='center', color='#7C3AED')

    # Hard Real-Time Alarm line: ITIC direct to Core 1 FreeRTOS
    ax.annotate('', xy=(11.3, 6.3), xytext=(7.3, 4.45),
                arrowprops=dict(arrowstyle="-|>", color='#DC2626', lw=2, linestyle='dashed'))
    ax.text(9.2, 5.7, "Direct HW IRQ (<10µs)", fontsize=7.5, fontweight='bold', color='#DC2626', rotation=15)

    # MSS -> External Network
    ax.annotate('', xy=(13.3, 1.55), xytext=(13.3, 2.05),
                arrowprops=dict(arrowstyle="<|-|>", color='#0284C7', lw=2))

    # Save outputs
    png_path = os.path.join(output_dir, "SYSTEM_BLOCK_DIAGRAM.png")
    pdf_path = os.path.join(output_dir, "SYSTEM_BLOCK_DIAGRAM.pdf")
    
    plt.tight_layout()
    plt.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.savefig(pdf_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    
    print(f"Generated diagram PNG: {png_path}")
    print(f"Generated diagram PDF: {pdf_path}")

if __name__ == "__main__":
    out_dir = r"d:\College\Power Sentry\docs"
    draw_system_block_diagram(out_dir)
