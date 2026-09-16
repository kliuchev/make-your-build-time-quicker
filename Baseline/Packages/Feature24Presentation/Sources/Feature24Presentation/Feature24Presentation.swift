import Feature24Domain
import Feature24Data

public enum Feature24PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature24DomainModel = Feature24DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
