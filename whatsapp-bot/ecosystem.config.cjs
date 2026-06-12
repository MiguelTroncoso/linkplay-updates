// Configuración de PM2 para mantener el bot vivo en el VPS.
// Uso: pm2 start ecosystem.config.js && pm2 save && pm2 startup
module.exports = {
  apps: [
    {
      name: 'iptv-bot',
      script: 'src/index.js',
      node_args: '--env-file=.env',
      max_memory_restart: '500M',
      restart_delay: 5000,
      autorestart: true,
      env: { NODE_ENV: 'production' },
    },
  ],
};
