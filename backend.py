from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load Bitlogicx data from JSON file
try:
    with open('bitlogicx_data.json', 'r') as file:
        bitlogicx_data = json.load(file)
except FileNotFoundError:
    # Default data if file not found
    bitlogicx_data = {
        "company": {
            "name": "Bitlogicx",
            "website": "https://bitlogicx.com/",
            "location": "A5 Commercial Block A, Architects Engineers Housing Society, Lahore, Pakistan",
            "contact_email": "contact@bitlogicx.com",
            "description": "Bitlogicx is a dedicated team of professionals delivering exceptional software services and innovative solutions to drive business success.",
            "social_media": {
                "LinkedIn": "https://www.linkedin.com/company/bitlogicx/",
                "Facebook": "#", 
                "Twitter": "#", 
                "Instagram": "#"
            },
            "sections": [
                "Home", "Services", "Products", "Projects", "About Us", 
                "Blogs", "Team", "Contact Us", "Career", "Hire A Professional"
            ],
            "offerings": {
                "free_consultation": True,
                "career_opportunities": True
            }
        },
        "products": [
            {
                "name": "Bitlogicx ERP",
                "description": "Empowers businesses to manage employee data and streamline processes with Slack integration for enhanced communication.",
                "use_case": "Business management and team collaboration"
            },
            {
                "name": "College/School Management System",
                "description": "Centralizes educational administration tasks, stakeholder communication, and student management.",
                "use_case": "Academic institutions"
            },
            {
                "name": "Learning Management System",
                "description": "User-friendly platform for online course delivery with flexibility and accessibility.",
                "use_case": "E-learning and education"
            },
            {
                "name": "Online Tourism Platform",
                "description": "Offers seamless booking, tailor-made itineraries, and personalized travel recommendations.",
                "use_case": "Travel and tourism"
            },
            {
                "name": "Inventory Management System",
                "description": "All-in-one application integrating inventory, purchases, sales, and warehouse management.",
                "use_case": "Retail and logistics"
            },
            {
                "name": "Restaurant POS",
                "description": "Manages orders, tableside service, and provides real-time analytics for restaurants.",
                "use_case": "Hospitality"
            },
            {
                "name": "Point of Sale System",
                "description": "Manages products, sales, purchases, and transactions with a seamless checkout experience.",
                "use_case": "Retail businesses"
            },
            {
                "name": "eCommerce Marketplace",
                "description": "Connects buyers and sellers with a diverse range of products and reliable support.",
                "use_case": "Online shopping"
            },
            {
                "name": "HR and Payroll Management",
                "description": "Automates HR processes, payroll calculations, and employee management tasks.",
                "use_case": "Human resources and payroll"
            }
        ],
        "services": {
            "general": "Custom software development and transformative business solutions",
            "specific": [
                "Software development",
                "System integration",
                "Business process automation",
                "Consultation services"
            ]
        },
        "custom_solutions": {
            "description": "We deliver tailor-made software solutions designed to address your unique business challenges",
            "development_process": [
                "Requirements Analysis",
                "Design and Architecture",
                "Development",
                "Testing and QA",
                "Deployment",
                "Maintenance and Support"
            ],
            "technologies": {
                "frontend": [
                    "React",
                    "Angular",
                    "Vue.js",
                    "Next.js",
                    "React Native"
                ],
                "backend": [
                    "Node.js",
                    "Python",
                    "Java",
                    "PHP",
                    ".NET"
                ],
                "database": [
                    "MySQL",
                    "PostgreSQL",
                    "MongoDB",
                    "SQL Server",
                    "Oracle"
                ],
                "cloud": [
                    "AWS",
                    "Azure",
                    "Google Cloud",
                    "Digital Ocean"
                ]
            },
            "industries_served": [
                "Healthcare",
                "Education",
                "E-commerce",
                "Finance",
                "Manufacturing",
                "Logistics",
                "Real Estate",
                "Travel & Tourism"
            ],
            "engagement_models": [
                {
                    "name": "Time and Material",
                    "description": "Flexible engagement model for projects with evolving requirements"
                },
                {
                    "name": "Fixed Price",
                    "description": "Predetermined cost and timeline for well-defined project scope"
                },
                {
                    "name": "Dedicated Team",
                    "description": "Dedicated resources working exclusively on your project"
                }
            ]
        },
        "response_templates": {
            "greeting": "Hi! I'm Bito, how can I help you today?",
            "company_intro": "We're Bitlogicx, a software company in Lahore creating innovative solutions for business success.",
            "contact": "You can email us at {contact_email} or visit us at {location}.",
            "response_styles": {
                "brief": "Here's what you need to know: {key_points}",
                "detailed": "Let me explain about {topic}: {explanation}",
                "technical": "Technical details: {specs}"
            }
        }
    }

# Helper function to check if a message contains any of the keywords
def contains_any(message, keywords):
    return any(keyword in message for keyword in keywords)

# Process user message and generate response
def process_message(message):
    normalized_message = message.lower()
    
    # Check for greetings
    if contains_any(normalized_message, ['hi', 'hello', 'hey', 'greetings']):
        return {
            "text": f"{bitlogicx_data['response_templates']['greeting']} I'm the Bitlogicx assistant ready to help you with information about our company and services.",
            "suggestions": [
                "What services do you offer?",
                "Tell me about your products",
                "How can I contact you?",
                "What technologies do you use?"
            ]
        }
    
    # Check for company info requests
    if contains_any(normalized_message, ['company', 'about', 'what is', 'who are', 'bitlogicx']):
        return {
            "text": bitlogicx_data['response_templates']['company_intro'] + " " + bitlogicx_data['company']['description'],
            "suggestions": [
                "What services do you offer?", 
                "Tell me about your products", 
                "Where is Bitlogicx located?"
            ]
        }
    
    # Check for location requests
    if contains_any(normalized_message, ['where', 'location', 'address', 'office']):
        return {
            "text": f"Bitlogicx is located at: {bitlogicx_data['company']['location']}",
            "suggestions": [
                "How can I contact you?",
                "What industries do you serve?",
                "What services do you offer?"
            ]
        }
    
    # Check for contact information requests
    if contains_any(normalized_message, ['contact', 'email', 'reach']):
        contact_msg = bitlogicx_data['response_templates']['contact']\
            .replace('{contact_email}', bitlogicx_data['company']['contact_email'])\
            .replace('{location}', bitlogicx_data['company']['location'])
        return {
            "text": contact_msg,
            "suggestions": [
                "Tell me about your services",
                "What industries do you work with?",
                "What products do you offer?"
            ]
        }
    
    # Check for services inquiries
    if contains_any(normalized_message, ['service', 'offer', 'provide', 'do you do']):
        services_msg = f"Our main focus is on {bitlogicx_data['services']['general']}. Specifically, we offer:"
        for service in bitlogicx_data['services']['specific']:
            services_msg += f"\n• {service}"
        
        return {
            "text": services_msg,
            "suggestions": [
                "Tell me more about custom solutions",
                "What technologies do you use?",
                "What industries do you serve?"
            ]
        }
    
    # Check for product inquiries
    if contains_any(normalized_message, ['product', 'solution', 'software', 'system', 'platform']):
        products_msg = "Here are some of our key products:\n\n"
        
        # Limit to showing just 3 products to avoid overwhelming the user
        display_products = bitlogicx_data['products'][:3]
        for product in display_products:
            products_msg += f"**{product['name']}**: {product['description']}\nUse case: {product['use_case']}\n\n"
        
        products_msg += "Would you like to know about more products or specific details about any of these?"
        
        return {
            "text": products_msg,
            "suggestions": [
                "Tell me about ERP",
                "Show me more products",
                "What technologies do you use?"
            ]
        }
    
    # Check for specific product inquiries
    for product in bitlogicx_data['products']:
        product_name_lower = product['name'].lower()
        use_case_lower = product['use_case'].lower()
        
        if any(term in normalized_message for term in [product_name_lower, use_case_lower]):
            return {
                "text": f"**{product['name']}**: {product['description']}\n\nUse case: {product['use_case']}",
                "suggestions": [
                    "Tell me about other products",
                    "What technologies do you use?",
                    "What services do you offer?"
                ]
            }
    
    # Check for technology stack inquiries
    if contains_any(normalized_message, ['tech', 'technology', 'stack', 'programming', 'language', 'framework']):
        tech = bitlogicx_data['custom_solutions']['technologies']
        tech_msg = "We work with a variety of technologies:\n\n"
        
        tech_msg += f"**Frontend:** {', '.join(tech['frontend'])}\n"
        tech_msg += f"**Backend:** {', '.join(tech['backend'])}\n"
        tech_msg += f"**Databases:** {', '.join(tech['database'])}\n"
        tech_msg += f"**Cloud:** {', '.join(tech['cloud'])}"
        
        return {
            "text": tech_msg,
            "suggestions": [
                "Tell me about your products",
                "What services do you offer?",
                "What industries do you serve?"
            ]
        }
    
    # Check for industries served
    if contains_any(normalized_message, ['industry', 'industries', 'sector', 'field', 'client']):
        industries_msg = "We serve clients across multiple industries including:"
        for industry in bitlogicx_data['custom_solutions']['industries_served']:
            industries_msg += f"\n• {industry}"
        
        return {
            "text": industries_msg,
            "suggestions": [
                "What services do you offer?",
                "Tell me about your products",
                "How can I contact you?"
            ]
        }
    
    # Check for development process
    if contains_any(normalized_message, ['process', 'methodology', 'approach', 'development']):
        process_msg = "Our development process includes these key phases:"
        for i, step in enumerate(bitlogicx_data['custom_solutions']['development_process']):
            process_msg += f"\n{i + 1}. {step}"
        
        return {
            "text": process_msg,
            "suggestions": [
                "What technologies do you use?",
                "Tell me about your products",
                "What services do you offer?"
            ]
        }
    
    # Check for career opportunities
    if contains_any(normalized_message, ['job', 'career', 'work', 'employment', 'hiring', 'opportunity']):
        if bitlogicx_data['company']['offerings']['career_opportunities']:
            career_msg = f"Yes, we have career opportunities available! Please visit our Careers page on our website or send your resume to {bitlogicx_data['company']['contact_email']}"
        else:
            career_msg = f"We don't have any open positions at the moment, but you can always send your resume to {bitlogicx_data['company']['contact_email']} for future opportunities."
        
        return {
            "text": career_msg,
            "suggestions": [
                "Tell me about your company",
                "What services do you offer?",
                "How can I contact you?"
            ]
        }
    
    # Check for consultation requests
    if contains_any(normalized_message, ['consult', 'consultation', 'advice', 'meeting', 'appointment']):
        if bitlogicx_data['company']['offerings']['free_consultation']:
            consult_msg = f"We offer free consultations! Please reach out to us at {bitlogicx_data['company']['contact_email']} to schedule a meeting with our experts."
        else:
            consult_msg = f"We'd be happy to set up a consultation. Please contact us at {bitlogicx_data['company']['contact_email']} for more information."
        
        return {
            "text": consult_msg,
            "suggestions": [
                "What services do you offer?",
                "Tell me about your products",
                "What technologies do you use?"
            ]
        }
    
    # Check for thanks/goodbye
    if contains_any(normalized_message, ['thank', 'thanks', 'bye', 'goodbye', 'see you']):
        return {
            "text": "You're welcome! If you have any more questions in the future, feel free to chat with us again. Have a great day!",
            "suggestions": []
        }
    
    # Default response for unrecognized queries
    return {
        "text": "I'm not sure I understand your question. Could you please rephrase or select one of these common topics?",
        "suggestions": [
            "What services do you offer?",
            "Tell me about your products",
            "How can I contact you?",
            "What technologies do you use?"
        ]
    }

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({
            'error': 'No message provided'
        }), 400
    
    response = process_message(user_message)
    return jsonify(response)

@app.route('/api/initial', methods=['GET'])
def initial_message():
    # Return initial greeting and suggestions
    return jsonify({
        "text": bitlogicx_data['response_templates']['greeting'],
        "suggestions": [
            "What services do you offer?",
            "Tell me about your products",
            "How can I contact you?",
            "What technologies do you use?"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)