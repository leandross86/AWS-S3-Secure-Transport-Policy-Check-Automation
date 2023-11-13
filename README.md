# AWS S3 Secure Transport Policy

Este script Python, projetado para ser executado como uma função AWS Lambda, aborda o Controle 2.1.1 do CIS Benchmark para AWS Foundations. Especificamente, este script verifica se todos os buckets S3 em uma conta têm uma política que inclui a condição `aws:SecureTransport`. Se uma política não contiver essa condição, o script adicionará ou atualizará a política do bucket para incluir essa condição.

## Mitigação

O controle 2.1.1 do CIS Benchmark visa garantir que as comunicações com o Amazon S3 sejam realizadas usando um transporte seguro (HTTPS). Ao negar explicitamente a ação S3 para solicitações que não usam transporte seguro, o script visa reforçar essa prática de segurança.

## Como Funciona

1. **Inicialização do Cliente S3**: O script inicializa um cliente S3 usando a biblioteca `boto3` da AWS.

2. **Listagem de Buckets**: Obtém a lista de todos os buckets na conta.

3. **Definição da Política Padrão**: Define uma política padrão que inclui a condição `aws:SecureTransport`.

4. **Iteração sobre os Buckets**: Itera sobre cada bucket na lista.

5. **Verificação da Existência do Bucket**: Verifica se o bucket realmente existe. Se não existir, imprime uma mensagem e passa para o próximo bucket.

6. **Obtenção da Política Atual do Bucket**: Obtém a política atual do bucket (se existir).

7. **Verificação da Condição `aws:SecureTransport` na Política**: Verifica se a política do bucket contém a condição `aws:SecureTransport`. Se não contiver, a condição é adicionada ou atualizada.

8. **Criação da Política Padrão se Necessário**: Se o bucket não tiver uma política, cria uma nova política usando a política padrão.

9. **Conclusão**: O script retorna uma mensagem indicando que a verificação e a atualização das políticas foram concluídas.

## Como Usar

1. **Configuração da Função Lambda**: Crie uma função Lambda na AWS e configure o script como o código da função.

2. **Configuração do Gatilho**: Adicione um gatilho para acionar a função Lambda conforme necessário (por exemplo, em um cronograma regular).

3. **Permissões IAM**: Certifique-se de que a função Lambda tenha as permissões adequadas para listar buckets, obter informações sobre buckets, obter e modificar políticas de bucket S3.

4. **Variáveis de Ambiente (Opcional)**: Se desejar personalizar a execução do script, pode-se adicionar variáveis de ambiente para configurar parâmetros, como região da AWS, etc.

5. **Logs e Monitoramento (Opcional)**: Configure logs e monitoramento conforme necessário para rastrear a execução da função Lambda.

**Nota:** Este script é fornecido como um ponto de partida e pode precisar ser adaptado conforme necessário para atender aos requisitos específicos do seu ambiente e políticas de segurança. Certifique-se de revisar e testar o script em um ambiente de desenvolvimento antes de implantá-lo em produção.
