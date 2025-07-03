from http.server import BaseHTTPRequestHandler
import json
import random

class InstagramHookGenerator:
    def __init__(self):
        self.hooks_templates = [
            "🔥 {topic} qui va changer votre {domain} !",
            "✨ Découvrez le secret de {topic}",
            "💡 Cette astuce {topic} va vous surprendre",
            "🚀 Prêt à maîtriser {topic} ?",
            "💎 Le guide ultime pour {topic}",
            "🌟 Pourquoi {topic} est si important",
            "⚡ {topic} : la méthode qui marche",
            "🎯 Attention : {topic} révélé !",
            "🔑 {topic} : voici comment faire",
            "💪 {topic} : relevez le défi !",
            "🎨 {topic} comme vous ne l'avez jamais vu",
            "🏆 Devenez expert en {topic}",
            "🔮 L'avenir de {topic} commence ici",
            "🌍 {topic} : la révolution est en marche",
            "⭐ {topic} : les secrets des pros",
            "🎭 {topic} : l'art de la perfection",
            "🌺 {topic} : révélez votre potentiel",
            "🎪 {topic} : le spectacle commence",
            "🌊 Surfez sur la vague {topic}",
            "🎵 {topic} : trouvez votre rythme"
        ]
        
        self.topics = [
            "fitness", "cuisine", "voyage", "mode", "tech", "lifestyle", 
            "beauté", "business", "art", "musique", "sport", "santé",
            "développement personnel", "entrepreneuriat", "créativité",
            "photographie", "design", "marketing", "éducation", "famille"
        ]
        
        self.domains = [
            "vie", "quotidien", "routine", "style", "approche", "vision", 
            "stratégie", "mindset", "parcours", "aventure", "expérience", "monde"
        ]
    
    def generate_hook(self, topic=None, domain=None):
        if not topic:
            topic = random.choice(self.topics)
        if not domain:
            domain = random.choice(self.domains)
            
        template = random.choice(self.hooks_templates)
        
        try:
            return template.format(topic=topic, domain=domain)
        except:
            return template.replace("{topic}", topic).replace("{domain}", domain)
    
    def generate_multiple_hooks(self, count=5, topic=None):
        # Assurer la diversité des templates
        hooks = []
        used_templates = set()
        
        for _ in range(count):
            attempts = 0
            while attempts < 10:  # Éviter les boucles infinies
                hook = self.generate_hook(topic=topic)
                template_base = hook.split(':')[0] if ':' in hook else hook.split(' ')[0]
                
                if template_base not in used_templates or len(used_templates) >= len(self.hooks_templates):
                    used_templates.add(template_base)
                    hooks.append(hook)
                    break
                attempts += 1
            
            # Si on n'a pas trouvé de template unique, ajouter quand même
            if len(hooks) < _ + 1:
                hooks.append(self.generate_hook(topic=topic))
        
        return hooks

# Initialiser le générateur
generator = InstagramHookGenerator()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Lire le corps de la requête
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Parser les données JSON
            data = json.loads(post_data.decode('utf-8'))
            
            topic = data.get('topic', '').strip()
            count = int(data.get('count', 5))
            
            # Limiter le nombre d'accroches
            count = min(count, 10)
            
            if not topic:
                topic = None
            
            # Générer les accroches
            hooks = generator.generate_multiple_hooks(count=count, topic=topic)
            
            # Préparer la réponse
            response = {
                'success': True,
                'hooks': hooks,
                'topic': topic if topic else 'aléatoire',
                'count': len(hooks)
            }
            
            # Envoyer la réponse
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            # Gérer les erreurs
            error_response = {
                'success': False,
                'error': str(e)
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Gérer les requêtes preflight CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
