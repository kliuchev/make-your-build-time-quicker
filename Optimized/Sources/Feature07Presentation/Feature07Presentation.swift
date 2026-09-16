import Feature07Domain
import Feature07Data

public enum Feature07PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature07DomainModel = Feature07DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
