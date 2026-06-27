def check_forecast_alerts(district, predictions, historical_avg=6.0):
    """
    Analyzes generated forecasts to detect ecological and hydrological risks.
    Returns a list of structured alert objects.
    """
    alerts = []
    if not predictions:
        return alerts
        
    # Threshold values (in meters below ground)
    CRITICAL_DEPTH_THRESHOLD_M = 8.5
    WARNING_DEPTH_THRESHOLD_M = 6.5
    
    # Extract prediction values at horizons
    predictions_map = {p["horizon"]: p for p in predictions}
    pred_7d = predictions_map.get("7d")
    pred_30d = predictions_map.get("30d")
    pred_3m = predictions_map.get("3m")
    pred_1y = predictions_map.get("1y")
    
    # 1. Check Safe Thresholds
    max_depth_pred = max(p["predicted_depth_m"] for p in predictions)
    max_depth_p = next(p for p in predictions if p["predicted_depth_m"] == max_depth_pred)
    
    if max_depth_pred >= CRITICAL_DEPTH_THRESHOLD_M:
        alerts.append({
            "type": "CRITICAL_THRESHOLD",
            "severity": "CRITICAL",
            "message": f"Groundwater level is predicted to fall below critical threshold ({max_depth_pred:.2f} m) in {max_depth_p['horizon']}.",
            "metric": f"{max_depth_pred:.2f} m",
            "remediation": "Impose strict limits on agricultural and industrial groundwater pumping immediately."
        })
    elif max_depth_pred >= WARNING_DEPTH_THRESHOLD_M:
        alerts.append({
            "type": "WARNING_THRESHOLD",
            "severity": "WARNING",
            "message": f"Groundwater level is predicted to approach depletion threshold ({max_depth_pred:.2f} m) in {max_depth_p['horizon']}.",
            "metric": f"{max_depth_pred:.2f} m",
            "remediation": "Recommend water conservation measures and optimize irrigation schedules."
        })
            
    # 2. Check Rapid Depletion Rates
    if pred_30d and pred_1y:
        # Check rate of change (depth increase in meters)
        depth_now = predictions[0]["predicted_depth_m"] # 7d or earliest
        depth_1y = pred_1y["predicted_depth_m"]
        annual_depletion = depth_1y - depth_now
        
        if annual_depletion >= 3.0:
            alerts.append({
                "type": "RAPID_DEPLETION",
                "severity": "CRITICAL",
                "message": f"Rapid depletion warning: Water table predicted to drop by {annual_depletion:.2f} meters within the next year.",
                "metric": f"+{annual_depletion:.2f} m/yr",
                "remediation": "Initiate community-wide water auditing and accelerate artificial aquifer recharge projects."
            })
        elif annual_depletion >= 1.5:
            alerts.append({
                "type": "RAPID_DEPLETION",
                "severity": "WARNING",
                "message": f"Moderate depletion trend: Water table predicted to drop by {annual_depletion:.2f} meters within the next year.",
                "metric": f"+{annual_depletion:.2f} m/yr",
                "remediation": "Advise crop rotation and shift to low-water crops (e.g. millets, pulses)."
            })

    # 3. Check Severe Drought Risk
    # High predicted depth combined with increasing temperature and zero rainfall
    if pred_3m:
        depth_3m = pred_3m["predicted_depth_m"]
        if depth_3m > historical_avg * 1.3:
            alerts.append({
                "type": "DROUGHT_RISK",
                "severity": "WARNING",
                "message": f"Elevated drought risk in {district} over the next 3 months due to declining water table.",
                "metric": "Low Aquifer Volume",
                "remediation": "Secure backup drinking water resources and optimize reservoir releases."
            })

    # 4. Check Recharge Opportunity
    # If predicted depth shows a significant decrease (table rising)
    if pred_30d and pred_3m:
        depth_30d = pred_30d["predicted_depth_m"]
        depth_3m = pred_3m["predicted_depth_m"]
        recharge_val = depth_30d - depth_3m # positive means depth at 3m is shallower than at 30d (rising table)
        
        if recharge_val >= 0.8:
            alerts.append({
                "type": "RECHARGE_OPPORTUNITY",
                "severity": "INFO",
                "message": "Aquifer recharge opportunity: Significant water table rise predicted due to seasonal inflows.",
                "metric": f"-{recharge_val:.2f} m (rising)",
                "remediation": "Maximize capture of surface runoff and optimize local percolation tanks."
            })
            
    return alerts
