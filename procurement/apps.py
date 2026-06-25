from django.apps import AppConfig


class ProcurementConfig(AppConfig):
    name = 'procurement'

    def ready(self):
        import procurement.signals
        from procurement.admin_security import AdminSecurityValidator
        
        # Validate admin security on startup
        try:
            AdminSecurityValidator.validate_admin_user()
        except Exception as e:
            import logging
            logger = logging.getLogger('procurepro.security')
            logger.error(f"Admin security validation failed on startup: {e}")

