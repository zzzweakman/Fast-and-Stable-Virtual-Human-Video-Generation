# AR measurement coverage

This clarification concerns implementation availability for the measurements performed on 15 October 2026.

Most surveyed AR-based methods had not released public implementations at measurement time. UniLS was the only open-source implementation we identified and could evaluate for the separate AR-component measurement. This describes the scope of our implementation search and evaluation at that time, rather than a permanent claim about all AR methods.

The [official UniLS repository](https://github.com/xg-chu/UniLS) provides audio-driven motion inference and visualization. Our measured run predicts motion and produces a FLAME visualization; it does not measure a native visual-AR or photorealistic appearance generator. Its runtime and memory therefore cannot characterize the AR category as a whole.

DyStream and Talker-T2AV are measured under render-based methods, following the survey's classification by the component that owns visual appearance. Their AR control components do not change that assignment.

The published numerical results and five blank pending entries are unchanged. The original measurement files, protocol and release manifest remain the same; this note adds the reason for the limited AR coverage.
