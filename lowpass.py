#!python

from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show


#------------------------------------------------
# Tạo ra một tín hiệu
#------------------------------------------------

sample_rate = 100.0
nsamples = 400
t = arange(nsamples) / sample_rate
x = cos(2*pi*0.5*t) + 0.2*sin(2*pi*2.5*t+0.1) + \
        0.2*sin(2*pi*15.3*t) + 0.1*sin(2*pi*16.7*t + 0.1) + \
            0.1*sin(2*pi*23.45*t+.8)


#------------------------------------------------
# Tạo ra bộ lọc FIR
#------------------------------------------------

# tỷ lệ Nyquist của tín hiệu.
nyq_rate = sample_rate / 2.0

# độ rộng mong muốn của quá trình chuyển từ pass tới stop,
#Chúng ta sẽ thiết kế bộ lọc với độ rộng 5 Hz
width = 5.0/nyq_rate

# Độ suy giảm mong muốn trong stop band, tính bằng dB.
ripple_db = 60.0

# Tính toán thứ tự và tham số Kaiser cho bộ lọc FIR
N, beta = kaiserord(ripple_db, width)

# Tần số cắt của bộ lọc
cutoff_hz = 10.0

# Dùng firwin với Kaiser window để tạo bộ lọc thông thấp FIR.
taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

# Dùng lfilter để lọc x với bộ lọc.
filtered_x = lfilter(taps, 1.0, x)

#------------------------------------------------
# Vẽ đáp ứng xung của bộ lọc FIR
#------------------------------------------------

figure(1)
plot(taps, 'bo-', linewidth=2)
title('Đáp ứng xung (%d taps)' % N)
grid(True)

#------------------------------------------------
# vẽ đáp ứng biên độ của bộ lọc
#------------------------------------------------

figure(2)
clf()
w, h = freqz(taps, worN=8000)
plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlabel('Tần số (kHz)')
ylabel('Cường độ')
title('Đáp ứng biên độ')
ylim(-0.05, 1.05)
grid(True)

# Vẽ phần trên
ax1 = axes([0.42, 0.6, .45, .25])
plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlim(0,8.0)
ylim(0.9985, 1.001)
grid(True)

# Vẽ phần dưới
ax2 = axes([0.42, 0.25, .45, .25])
plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlim(12.0, 20.0)
ylim(0.0, 0.0025)
grid(True)

#------------------------------------------------
# Vẽ tín hiệu góc và tín hiệu đã được lọc
#------------------------------------------------

# Độ trễ pha của tín hiệu đã được lọc
delay = 0.5 * (N-1) / sample_rate

figure(3)
# Tín hiệu góc
plot(t, x)
# Tín hiệu đã được lọc, dịch để bù cho pha bị trễ
plot(t-delay, filtered_x, 'r-')
plot(t[N-1:]-delay, filtered_x[N-1:], 'g', linewidth=4)

xlabel('t')
grid(True)

show()