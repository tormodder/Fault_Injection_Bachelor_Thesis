# New and improved instructions
- Run `clock_freq_server.py` (unglitched) or `clock_freq_glitches_server.py`
- Run `FFTdata_observer.py`
- Sit back and enjoy while I continue to work on floating point jittery signals

# Screenshots
Pure integer signal with FFT analysis - 507 samples
![Pure integer signal with FFT analysis](screenshots/Integer_clock_with_FFT_507_samples.png)

Pure integer glitched signal with FFT analysis - 510 samples
![Pure integer glitched signal with FFT analysis](screenshots/Integer_clock_with_glitches_with_FFT_510_samples.png)

Pure integer glitched signal with FFT analysis - 832 samples
![Pure integer glitched signal with FFT analysis with increased sample size](screenshots/Integer_clock_with_glitches_with_FFT_832_samples.png)

---

# Old Instructions

- Run `python ./clock_freq_floatstream_glitches_server.py` first
- Run `python ./ clock_observer_statistical_data_extractor.py` second
- Let run for a bit to collect data
- Close the window showing the servers output
- The observer will do its FFT analysis and create a plot

# Old Screenshots
Clock with jitter
![Clock with jitter](screenshots/Clock_jitter_server.png)

Clock with jitter and glitch
![Clock with jitter and glitch](screenshots/Clock_jitter_server_with_glitch.png)

Observer FFT analysis output plot
![Observer FFT analysis output plot](screenshots/Observer_FFT_analysis_output.png)