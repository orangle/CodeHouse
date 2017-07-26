%option noyywrap
%{
	int chars = 0;
	int words = 0;
	int lines = 0;
%}

%%
[a-zA-Z]+ { words++; chars += strlen(yytext); }
\n        { chars++; lines++; }
.         { chars++;}
%%

main(argc, argv)
int argc;
char **argv;
{
	if (argc > 1){
		if(!(yyin = fopen(argv[1], "r"))){
			perror(argv[1]);
			return (1);
		}
	}

	yylex();
	printf("%8d%8d%8d\n", lines, words, chars);
}
