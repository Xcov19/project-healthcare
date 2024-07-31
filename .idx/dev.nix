# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env

{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    # pkgs.go
    pkgs.python312
    # pkgs.python311Packages.pip
    pkgs.poetry
    pkgs.nodejs_20
    pkgs.ruff
    pkgs.gnumake
    # pkgs.docker
    # pkgs.nodePackages.nodemon
  ];

  # Services
    services.docker.enable = true;


  # Sets environment variables in the workspace
  env = { };
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      # "vscodevim.vim"
      "ms-azuretools.docker"
      "eamodio.gitlens"
      "ebenjs.vampire-ebenjs"
      "GitHub.vscode-pull-request-github"
      "mgesbert.python-path"
      "ms-azuretools.vscode-docker"
      "ms-python.isort"
      "njqdev.vscode-python-typehint"
      "solomonkinard.todos"
      "ms-python.black-formatter"
      "ms-python.debugpy"
      "ms-python.python"
      "bungcip.better-toml"
      "sourcery.sourcery"
    ];

    
    # Enable previews
    previews = {
      enable = true;
      previews = {
        # web = {
        #   # Example: run "npm run dev" with PORT set to IDX's defined port for previews,
        #   # and show it in IDX's web preview panel
        #   command = ["npm" "run" "dev"];
        #   manager = "web";
        #   env = {
        #     # Environment variables to set for your server
        #     PORT = "$PORT";
        #   };
        # };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # Example: install JS dependencies from NPM
        # npm-install = "npm install";
        poetry-install = "poetry install --no-root --with=dev --sync -v";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # Example: start a background task to watch and re-build backend code
        # watch-backend = "npm run watch-backend";
        poetry-install = "poetry install --no-root --with=dev --sync -v";
        poetry-use = "poetry env use python3";
        # npm-install = "npm install xcov19/package.json";
      };
    };
  };
}
