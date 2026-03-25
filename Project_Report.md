🚦 Project Report: SmartFlow AI
Edge Vision for Adaptive Traffic Management

Course: AI & Machine Learning Capstone (BYOP)				Creator: Acheev.D 

Executive Summary
Urban traffic congestion is a globally recognized crisis, resulting in billions of hours of lost productivity, catastrophic environmental damage through excess CO2 emissions, and delayed emergency response times. SmartFlow AI was developed to solve this issue without requiring cities to invest in expensive new hardware. By leveraging state-of-the-art Computer Vision (YOLOv8) and Edge Computing, SmartFlow transforms existing "dumb" CCTV cameras into intelligent sensors. This report details the engineering journey, architectural decisions, and machine learning concepts applied to build this cyber-physical system.
1. The Problem: Why It Matters
Currently, over 80% of urban traffic signals operate on static, fixed timers. This rigid architecture is fundamentally flawed:
Massive Fuel Waste: Vehicles are forced to idle at red lights even when intersecting lanes are completely empty. An average idling car burns 0.9 liters of fuel per hour.
Emergency Delays: Ambulances and fire engines get trapped in artificial gridlock, often losing the critical "Golden Hour" for patient care.
The Hardware Barrier: Traditional "smart" upgrades require cities to dig up roads to install expensive inductive loops or LiDAR sensors, hindering widespread adoption.
2. Our Approach: The ML Solution
Our goal was to build a hardware-agnostic software layer. The solution is divided into two core components:
The Edge ML Sensor (Python/YOLOv8): Instead of relying on physical road sensors, we use the yolov8n.pt (Nano) model via OpenCV to process real-time RTSP video streams. The model detects vehicles within a specific "Region of Interest" (ROI) and calculates a real-time metric called Lane Pressure (density * wait time).
The Digital Twin Decision Engine (JavaScript/HTML5): To safely test the ML logic without accessing a physical intersection, we built a high-fidelity Digital Twin simulation. The engine takes the Lane Pressure data and feeds it into a heuristic state machine that dynamically actuates the traffic lights.
Core Features Developed:
🚑 Emergency Preemption: The AI assigns an absolute priority score of 1000 to detect emergency vehicles, triggering a safe "Green Corridor" clearance phase.
🌍 Carbon Footprint Tracker: Live calculation of idle-time reduction, estimating real-world drops in kg CO2 per hour.
🛡️ Fail-Safe Weather Protocol: A simulated degradation protocol. If camera visibility drops below a safe threshold (e.g., heavy fog), the AI gracefully suspends itself and hands control back to the baseline fixed timer.
3. Key Architectural Decisions
As both engineers and project strategists, several crucial decisions were made to ensure the system was viable for real-world deployment:
Decision A: Edge Computing over Cloud Processing
Initially, we considered sending the video feeds to a centralized cloud server (like AWS or GCP) for inference. However, we pivoted to Edge AI (processing the video locally on devices like an NVIDIA Jetson Nano on the traffic pole).
Why: Sending 1080p video from hundreds of intersections requires massive bandwidth and introduces latency. Edge computing ensures ultra-low latency (critical for traffic safety), operates without an internet connection, and preserves citizen privacy by never storing or transmitting raw video footage.
Decision B: Heuristic State Machine over Pure Reinforcement Learning (RL)
While an RL agent could theoretically learn optimal traffic patterns, we opted for a Heuristic State Machine driven by ML vision data.
Why: Cyber-physical systems (where code controls heavy physical machinery) require explainability and safety guarantees. A heuristic approach allowed us to hard-code non-negotiable safety rules (e.g., minimum pedestrian walk times, mandatory yellow light durations) that a "black box" neural network might attempt to bypass to optimize flow.
4. Challenges Faced & Overcome
Challenge: The "Speeding Car" Dilemma (Max-Out Problem)
The Issue: During simulation testing, we encountered a flaw in the optimization logic. If the AI strictly rewarded "moving traffic," a constant stream of speeding cars on a main avenue would cause the AI to hold the green light infinitely, completely starving the cross-traffic lanes.
The Solution: We implemented a "Max Green Hard Limit" heuristic. Once a light has been green for a maximum threshold, the AI forces a phase switch regardless of the Lane Pressure on the main avenue. This ensures fairness and prevents infinite starvation.
Challenge: The Simulation-to-Reality Gap
The Issue: Proving that Python bounding boxes could successfully translate into physical traffic improvements.
The Solution: Building the Digital Twin. We had to program realistic car physics (acceleration, braking distance, reaction times) in JavaScript so the simulation accurately reflected how real traffic would behave when the AI switched the lights.
5. What We Learned
This capstone pushed us far beyond training models on static datasets. Key takeaways include:
Systems Integration: We learned the profound difference between a standalone Machine Learning model and an integrated AI product. Getting YOLOv8 to detect a car is easy; using that detection to safely control a traffic light is a complex systems engineering challenge.
Managing False Positives: We learned how to handle AI uncertainty. By implementing the "Fail-Safe Protocol" for low visibility, we learned that good AI engineering means knowing when not to trust the AI.
6. Future Scope
If taken beyond the capstone phase, the next iteration of SmartFlow would include:
V2X Communication: Allowing the traffic light to broadcast its current state and time-to-red directly to approaching autonomous vehicles.
City-Wide Mesh: Connecting individual Edge nodes so that intersection A can warn intersection B of an approaching heavy platoon or ambulance, creating a synchronized "green wave" across the city.

Prepared by: Acheev.D
Status: Ready for Deployment Pilot
