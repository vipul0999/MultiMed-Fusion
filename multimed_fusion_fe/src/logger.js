
const isDev = process.env.NODE_ENV === "development";


const logger = {
  info: (message, ...optionalParams) => {
    console.info(`ℹ️ INFO: ${message}`, ...optionalParams);
  },
  warn: (message, ...optionalParams) => {
    console.warn(`⚠️ WARN: ${message}`, ...optionalParams);
  },
  error: (message, ...optionalParams) => {
    console.error(`❌ ERROR: ${message}`, ...optionalParams);
  },
  debug: (message, ...optionalParams) => {
    if (isDev) {
      console.debug(`🐛 DEBUG: ${message}`, ...optionalParams);
    }
  }
};

export default logger;
