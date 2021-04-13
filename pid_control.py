class PID:
    def __init__(self, time: float, k_p: float, k_i: float, k_d: float, tau: float, lim_min: float, lim_max: float):
        # Controller gains
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_i
        # Derivative low-pass filter time constant
        self.tau = tau
        # Output limits
        self.lim_min = lim_min
        self.lim_max = lim_max
        # sample time
        self.t = time
        # controller memory
        self.integrator = 0.0
        self.prev_err = 0.0
        self.differentiator = 0.0
        self.prev_meas = 0.0
        # output
        self.out = 0.0

    @property
    def k_p(self):
        return self.k_p

    @property
    def k_i(self):
        return self.k_i

    @property
    def k_d(self):
        return self.k_d

    @property
    def out(self):
        return self.out

    @k_p.setter
    def k_p(self, var: float):
        self.k_p = var

    @k_i.setter
    def k_i(self, var: float):
        self.k_i = var

    @k_d.setter
    def k_d(self, var: float):
        self.k_d = var

    def update(self, setpoint: float, measurement: float):
        # signal error
        error = setpoint - measurement
        # prportional
        proportional = self.k_p * error
        # integral
        self.integrator += 0.5 * self.k_i * self.t * (error + self.prev_err)
        # anti-wind-up via dynamic integrator clamping
        lim_max_int, lim_min_int = 0.0, 0.0
        if self.lim_max > proportional:
            lim_max_int = self.lim_max - proportional
        if self.lim_min < proportional:
            lim_min_int = self.lim_min - proportional
        # clamp integrator
        if self.integrator > lim_max_int:
            self.integrator = lim_max_int
        elif self.integrator < lim_min_int:
            self.integrator = lim_min_int
        # derivative (dand-limited diferentiator)
        diff_1 = (2.0 * self.k_d * (measurement - self.differentiator))
        diff_2 = (2.0 * self.tau - self.t) * self.differentiator
        diff_3 = (2.0 * self.tau + self.t)
        self.differentiator = diff_1 + diff_2 / diff_3
        # output and apply limits
        self.out = proportional + self.integrator + self.differentiator
        if self.out > self.lim_max:
            self.out = self.lim_max
        elif self.out < self.lim_min:
            self.out = self.lim_min
        # saving previous data
        self.prev_err = error
        self.prev_meas = measurement

        return self.out
