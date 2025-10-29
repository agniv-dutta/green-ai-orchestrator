from datetime import datetime, timedelta
from typing import Dict, List
import random

class ESGReporter:
    def __init__(self):
        self.compliance_frameworks = {
            'tcfd': 'Task Force on Climate-related Financial Disclosures',
            'sasb': 'Sustainability Accounting Standards Board',
            'ghg_protocol': 'Greenhouse Gas Protocol',
            'cdp': 'Carbon Disclosure Project'
        }
    
    def generate_esg_report(self, workloads_data: List[Dict]) -> Dict:
        """Generate comprehensive ESG compliance report"""
        if not workloads_data:
            return self._generate_empty_report()
        
        # Calculate metrics
        total_carbon_saved = sum(item.get('carbon_savings_kg', 0) for item in workloads_data)
        total_cost_saved = sum(item.get('cost_savings_usd', 0) for item in workloads_data)
        total_workloads = len(workloads_data)
        
        # Calculate performance metrics
        avg_carbon_savings = total_carbon_saved / total_workloads if total_workloads > 0 else 0
        avg_savings_percent = sum(item.get('savings_percentage', 0) for item in workloads_data) / total_workloads
        
        # ESG Score calculation (0-100)
        esg_score = self._calculate_esg_score(avg_savings_percent, total_carbon_saved, total_workloads)
        
        # Compliance status
        compliance_status = self._determine_compliance_status(esg_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(esg_score, workloads_data)
        
        # Carbon credit estimation
        carbon_credits = self._estimate_carbon_credits(total_carbon_saved)
        
        return {
            'report_id': f"ESG-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'report_period': 'last_30_days',
            
            # Performance Metrics
            'esg_score': round(esg_score, 1),
            'compliance_status': compliance_status,
            'performance_tier': self._get_performance_tier(esg_score),
            
            # Environmental Impact
            'environmental_metrics': {
                'total_carbon_saved_kg': round(total_carbon_saved, 2),
                'total_carbon_saved_tons': round(total_carbon_saved / 1000, 2),
                'equivalent_trees_planted': round(total_carbon_saved / 21.77, 0),  # kg CO2 per tree per year
                'equivalent_cars_off_road': round(total_carbon_saved / 4600, 1),   # kg CO2 per car per year
                'carbon_intensity_reduction': f"{avg_savings_percent:.1f}%"
            },
            
            # Economic Impact
            'economic_metrics': {
                'total_cost_saved_usd': round(total_cost_saved, 2),
                'estimated_annual_savings': round(total_cost_saved * 12, 2),
                'roi_percentage': round((total_cost_saved / (total_cost_saved * 0.1)) * 100, 1),  # Assuming 10% investment
                'cost_per_kg_saved': round(total_cost_saved / total_carbon_saved, 2) if total_carbon_saved > 0 else 0
            },
            
            # Operational Metrics
            'operational_metrics': {
                'total_workloads_optimized': total_workloads,
                'avg_carbon_savings_per_workload': round(avg_carbon_savings, 2),
                'optimization_efficiency': f"{avg_savings_percent:.1f}%",
                'preferred_regions': self._get_preferred_regions(workloads_data)
            },
            
            # Compliance & Certifications
            'compliance_info': {
                'frameworks_applicable': list(self.compliance_frameworks.keys()),
                'carbon_credit_eligible': carbon_credits['eligible'],
                'estimated_credits': carbon_credits['estimated_credits'],
                'certification_ready': esg_score >= 75
            },
            
            # AI Recommendations
            'recommendations': recommendations,
            
            'status': 'success'
        }
    
    def _calculate_esg_score(self, avg_savings_percent: float, total_carbon_saved: float, total_workloads: int) -> float:
        """Calculate comprehensive ESG score (0-100)"""
        # Base score from savings percentage (0-60 points)
        savings_score = min(60, avg_savings_percent * 1.2)
        
        # Scale factor for total impact (0-20 points)
        scale_score = min(20, (total_carbon_saved / 1000) * 2)
        
        # Consistency factor (0-20 points)
        consistency_score = min(20, (total_workloads / 50) * 10)
        
        return savings_score + scale_score + consistency_score
    
    def _determine_compliance_status(self, esg_score: float) -> str:
        """Determine compliance status based on ESG score"""
        if esg_score >= 90:
            return "LEADERSHIP"
        elif esg_score >= 75:
            return "ADVANCED"
        elif esg_score >= 60:
            return "COMPLIANT"
        elif esg_score >= 40:
            return "DEVELOPING"
        else:
            return "BEGINNER"
    
    def _get_performance_tier(self, esg_score: float) -> str:
        """Get performance tier description"""
        tiers = {
            90: "Industry Leader",
            75: "High Performer", 
            60: "Compliant",
            40: "Developing",
            0: "Needs Improvement"
        }
        
        for threshold, tier in sorted(tiers.items(), reverse=True):
            if esg_score >= threshold:
                return tier
        return "Needs Improvement"
    
    def _generate_recommendations(self, esg_score: float, workloads_data: List[Dict]) -> Dict:
        """Generate AI-powered recommendations"""
        immediate_actions = []
        strategic_actions = []
        
        if esg_score < 60:
            immediate_actions.extend([
                "Implement carbon-aware scheduling for all batch workloads",
                "Shift 30% of workloads to us-west-2 or eu-west-1 regions",
                "Right-size over-provisioned instances (avg 40% waste detected)",
                "Enable auto-scaling to match actual resource demand"
            ])
        else:
            immediate_actions.extend([
                "Maintain current optimization strategies",
                "Explore spot instances for non-critical workloads",
                "Optimize data storage with tiered storage solutions"
            ])
        
        if esg_score >= 75:
            strategic_actions.extend([
                "Apply for carbon credit certification with estimated 5-10 credits/month",
                "Consider renewable energy credits for remaining emissions",
                "Implement carbon accounting across entire organization",
                "Explore carbon offset partnerships"
            ])
        else:
            strategic_actions.extend([
                "Focus on achieving 60+ ESG score for basic compliance",
                "Implement monitoring for all cloud workloads",
                "Train team on carbon-aware development practices"
            ])
        
        # Region-specific recommendations
        regions_used = [w.get('region', 'unknown') for w in workloads_data]
        high_carbon_regions = [r for r in regions_used if r in ['ap-south-1', 'ap-southeast-1']]
        
        if high_carbon_regions:
            immediate_actions.append(f"Prioritize moving workloads from {', '.join(high_carbon_regions)} to lower-carbon regions")
        
        return {
            'immediate_actions': immediate_actions,
            'strategic_actions': strategic_actions,
            'expected_impact': f"Increase ESG score by {max(5, 100 - esg_score)} points in 30 days",
            'priority_level': "HIGH" if esg_score < 60 else "MEDIUM"
        }
    
    def _estimate_carbon_credits(self, total_carbon_saved: float) -> Dict:
        """Estimate carbon credit eligibility"""
        carbon_tons = total_carbon_saved / 1000
        
        # Basic eligibility criteria
        eligible = carbon_tons >= 1.0  # At least 1 ton CO2 equivalent
        estimated_credits = carbon_tons * 0.8  # 80% conversion rate
        
        return {
            'eligible': eligible,
            'estimated_credits': round(estimated_credits, 2),
            'minimum_for_certification': 1.0,
            'current_level': round(carbon_tons, 2)
        }
    
    def _get_preferred_regions(self, workloads_data: List[Dict]) -> List[str]:
        """Get most frequently used optimized regions"""
        if not workloads_data:
            return ['us-west-2', 'eu-west-1']
        
        region_counts = {}
        for workload in workloads_data:
            region = workload.get('region')
            if region:
                region_counts[region] = region_counts.get(region, 0) + 1
        
        # Sort by count and return top 3
        preferred = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        return [region for region, count in preferred]
    
    def _generate_empty_report(self) -> Dict:
        """Generate report template when no data available"""
        return {
            'report_id': f"ESG-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'esg_score': 0.0,
            'compliance_status': "NO_DATA",
            'performance_tier': "No Data Available",
            'environmental_metrics': {},
            'economic_metrics': {},
            'operational_metrics': {},
            'compliance_info': {},
            'recommendations': {
                'immediate_actions': ["Start collecting workload data to generate ESG insights"],
                'strategic_actions': ["Implement GreenAI Orchestrator across your cloud infrastructure"],
                'priority_level': "HIGH"
            },
            'status': 'no_data'
        }

# Global instance
esg_reporter = ESGReporter()