import Feature02Domain
import Feature02Data

public enum Feature02PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature02DomainModel = Feature02DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
