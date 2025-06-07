#!/usr/bin/env python3
"""
Deploy Enhanced News System to Web Server
Generates the site locally and copies to current directory for web access
"""

import os
import sys
import shutil
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from article_enhancer import EnhancedRealNewsSystem

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def deploy_enhanced_site():
    """Deploy the enhanced news site with category navigation"""
    try:
        logger.info("🚀 Starting enhanced news site deployment...")
        
        # Generate site in current directory for web access
        current_dir = Path('.')
        system = EnhancedRealNewsSystem(current_dir)
        system.generate_enhanced_news_website()
        
        # Check if files were created
        index_file = current_dir / 'index.html'
        if index_file.exists():
            logger.info(f"✅ Site deployed successfully to {index_file.absolute()}")
            logger.info(f"📊 File size: {index_file.stat().st_size} bytes")
            
            # Also create a backup in test_output for reference
            test_output = Path('test_output')
            test_output.mkdir(exist_ok=True)
            if (current_dir / 'index.html').exists():
                shutil.copy2(current_dir / 'index.html', test_output / 'index.html')
                logger.info(f"📋 Backup created in {test_output}")
            
        else:
            logger.error("❌ Failed to create index.html file")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"💥 Deployment failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = deploy_enhanced_site()
    if success:
        print("\n🎉 Enhanced news site with category navigation deployed successfully!")
        print("📂 Files are now in the current directory and ready for web access")
        print("🔄 The site should now update when you refresh your browser")
    else:
        print("\n❌ Deployment failed. Check the logs above for details.")
        sys.exit(1)